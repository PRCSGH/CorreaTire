# © 2021 onDevelop.SA
# Autor: Idelis Gé Ramírez

from odoo import models, api, fields, _
from odoo.tools.misc import format_date

from dateutil.relativedelta import relativedelta
from itertools import chain


class AccountCashFlowReport(models.AbstractModel):

    _inherit = "account.cash.flow.report"

    @api.model
    def _get_liquidity_move_report_lines(self, options, currency_table_query, payment_move_ids, payment_account_ids):
        ''' Fetch all information needed to compute lines from liquidity moves.
        The difficulty is to represent only the not-reconciled part of balance.

        :param options:                 The report options.
        :param currency_table_query:    The floating query to handle a multi-company/multi-currency environment.
        :param payment_move_ids:        A tuple containing all account.move's ids being the liquidity moves.
        :param payment_account_ids:     A tuple containing all account.account's ids being used in a liquidity journal.
        :return:                        A list of tuple (account_id, account_code, account_name, account_internal_type, amount).
        '''
        if not payment_move_ids:
            return []

        reconciled_amount_per_account = {}

        # ==== Compute the reconciled part of each account ====

        query = '''
            SELECT
                credit_line.account_id,
                account.code,
                COALESCE(NULLIF(ir_translation.value, ''),
                account.name) account_name,
                account.internal_type,
                SUM(ROUND(partial.amount * currency_table.rate, currency_table.precision))
            FROM account_move_line credit_line
            LEFT JOIN ''' + currency_table_query + ''' ON currency_table.company_id = credit_line.company_id
            LEFT JOIN account_partial_reconcile partial ON partial.credit_move_id = credit_line.id
            JOIN account_account account ON account.id = credit_line.account_id
            LEFT JOIN ir_translation ON ir_translation.name = 'account.account,name' AND ir_translation.res_id = account.id AND ir_translation.type = 'model' AND ir_translation.lang = %s
            WHERE credit_line.move_id IN %s AND credit_line.account_id NOT IN %s
            AND partial.max_date BETWEEN %s AND %s
            GROUP BY credit_line.company_id, credit_line.account_id, account.code, account_name, account.internal_type
            
            UNION ALL
            
            SELECT
                debit_line.account_id,
                account.code,
                account_move_line.ref as bill_reference,
                COALESCE(NULLIF(ir_translation.value, ''), account.name) account_name,
                account.internal_type,
                -SUM(ROUND(partial.amount * currency_table.rate, currency_table.precision))
            FROM account_move_line debit_line
            LEFT JOIN ''' + currency_table_query + ''' ON currency_table.company_id = debit_line.company_id
            LEFT JOIN account_partial_reconcile partial ON partial.debit_move_id = debit_line.id
            JOIN account_account account ON account.id = debit_line.account_id
            LEFT JOIN ir_translation ON ir_translation.name = 'account.account,name' AND ir_translation.res_id = account.id AND ir_translation.type = 'model' AND ir_translation.lang = %s
            WHERE debit_line.move_id IN %s AND debit_line.account_id NOT IN %s
            AND partial.max_date BETWEEN %s AND %s
            GROUP BY debit_line.company_id, debit_line.account_id, account.code, account_name, account.internal_type
        '''
        self._cr.execute(query, [
            self.env.user.lang, payment_move_ids, payment_account_ids, options['date']['date_from'], options['date']['date_to'],
            self.env.user.lang, payment_move_ids, payment_account_ids, options['date']['date_from'], options['date']['date_to'],
        ])

        for account_id, account_code, account_name, account_internal_type, reconciled_amount in self._cr.fetchall():
            reconciled_amount_per_account.setdefault(account_id, [account_code, account_name, account_internal_type, 0.0, 0.0])
            reconciled_amount_per_account[account_id][3] += reconciled_amount

        # ==== Compute total amount of each account ====

        query = '''
            SELECT
                line.account_id,
                account.code,
                COALESCE(NULLIF(ir_translation.value, ''), account.name) account_name,
                account.internal_type,
                SUM(ROUND(line.balance * currency_table.rate, currency_table.precision))
            FROM account_move_line line
            LEFT JOIN ''' + currency_table_query + ''' ON currency_table.company_id = line.company_id
            JOIN account_account account ON account.id = line.account_id
            LEFT JOIN ir_translation ON ir_translation.name = 'account.account,name' AND ir_translation.res_id = account.id AND ir_translation.type = 'model' AND ir_translation.lang = %s
            WHERE line.move_id IN %s AND line.account_id NOT IN %s
            GROUP BY line.account_id, account.code, account_name, account.internal_type
        '''
        self._cr.execute(query, [self.env.user.lang, payment_move_ids, payment_account_ids])

        for account_id, account_code, account_name, account_internal_type, balance in self._cr.fetchall():
            reconciled_amount_per_account.setdefault(account_id, [account_code, account_name, account_internal_type, 0.0, 0.0])
            reconciled_amount_per_account[account_id][4] += balance

        return [(k, v[0], v[1], v[2], v[4] + v[3]) for k, v in reconciled_amount_per_account.items()]


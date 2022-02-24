# © 2021 onDevelop.SA
# Autor: Idelis Gé Ramírez

from odoo import models, api, fields, _
from odoo.tools.misc import format_date

from dateutil.relativedelta import relativedelta
from itertools import chain


class MulticurrencyRevaluationReport(models.Model):

    _inherit = "account.multicurrency.revaluation"

    bill_reference = fields.Char()

    def _get_sql(self):
        options = self.env.context['report_options']
        query = '(VALUES {}) AS custom_currency_table(currency_id, rate)'.format(
            ', '.join("(%s, %s)" for i in range(len(options['currency_rates'])))
        )
        params = list(chain.from_iterable((cur['currency_id'], cur['rate']) for cur in options['currency_rates'].values()))
        custom_currency_table = self.env.cr.mogrify(query, params).decode(self.env.cr.connection.encoding)

        return """
            SELECT {move_line_fields},
                   aml.amount_currency                                  AS report_amount_currency,
                   aml.balance                                          AS report_balance,
                   aml.amount_currency / custom_currency_table.rate               AS report_amount_currency_current,
                   aml.amount_currency / custom_currency_table.rate - aml.balance AS report_adjustment,
                   aml.currency_id                                      AS report_currency_id,
                   account.code                                         AS account_code,
                   account.name                                         AS account_name,
                   account_move.ref                                AS bill_reference,
                   currency.name                                        AS currency_code,
                   move.ref                                             AS move_ref,
                   move.name                                            AS move_name,
                   NOT EXISTS (
                       SELECT * FROM account_account_exclude_res_currency_provision WHERE account_account_id = account_id AND res_currency_id = aml.currency_id
                   )                                                    AS report_include
            FROM account_move_line aml
            JOIN account_move move ON move.id = aml.move_id
            JOIN account_account account ON aml.account_id = account.id
            JOIN res_currency currency ON currency.id = aml.currency_id
            JOIN {custom_currency_table} ON custom_currency_table.currency_id = currency.id
            WHERE (account.currency_id != aml.company_currency_id OR (account.internal_type IN ('receivable', 'payable') AND (aml.currency_id != aml.company_currency_id)))

            UNION ALL

            -- Add the lines without currency, i.e. payment in company currency for invoice in foreign currency
            SELECT {move_line_fields},
                   CASE WHEN aml.id = part.credit_move_id THEN -part.debit_amount_currency ELSE -part.credit_amount_currency
                   END                                                  AS report_amount_currency,
                   -part.amount                                         AS report_balance,
                   CASE WHEN aml.id = part.credit_move_id THEN -part.debit_amount_currency ELSE -part.credit_amount_currency
                   END / custom_currency_table.rate                               AS report_amount_currency_current,
                   CASE WHEN aml.id = part.credit_move_id THEN -part.debit_amount_currency ELSE -part.credit_amount_currency
                   END / custom_currency_table.rate - aml.balance                 AS report_adjustment,
                   CASE WHEN aml.id = part.credit_move_id THEN part.debit_currency_id ELSE part.credit_currency_id
                   END                                                  AS report_currency_id,
                   account.code                                         AS account_code,
                   account.name                                         AS account_name,
                   account_move.ref                                     AS bill_reference,
                   currency.name                                        AS currency_code,
                   move.ref                                             AS move_ref,
                   move.name                                            AS move_name,
                   NOT EXISTS (
                       SELECT * FROM account_account_exclude_res_currency_provision WHERE account_account_id = account_id AND res_currency_id = aml.currency_id
                   )                                                    AS report_include
            FROM account_move_line aml
            JOIN account_move move ON move.id = aml.move_id
            JOIN account_account account ON aml.account_id = account.id
            JOIN account_partial_reconcile part ON aml.id = part.credit_move_id OR aml.id = part.debit_move_id
            JOIN res_currency currency ON currency.id = (CASE WHEN aml.id = part.credit_move_id THEN part.debit_currency_id ELSE part.credit_currency_id END)
            JOIN {custom_currency_table} ON custom_currency_table.currency_id = currency.id
            WHERE (account.currency_id = aml.company_currency_id AND (account.internal_type IN ('receivable', 'payable') AND aml.currency_id = aml.company_currency_id))
        """.format(
            custom_currency_table=custom_currency_table,
            move_line_fields=self._get_move_line_fields('aml'),
        )
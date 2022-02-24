# © 2021 onDevelop.sa
# Autor: Idelis Gé Ramírez

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    is_remittance = fields.Boolean(compute='compute_remittance', store=True)

    @api.depends('reconciled_invoices_count')
    def compute_remittance(self):
            '''Compute if the related invoices are more than 8 and set true if.'''
            for payment in self:
                if (len(payment.reconciled_bill_ids) > 8 and
                    payment.payment_type == 'outbound'):
                    payment.is_remittance = True
#     def compute_remittance(self):
#         '''Compute if the related invoices are more than 8 and set true if.'''
#         for payment in self:
#             if len(payment.reconciled_invoice_ids) > 8:
#                 payment.is_remittance = True

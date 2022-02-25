# -*- coding: utf-8 -*-
# from odoo import http


# class RemittancePayments(http.Controller):
#     @http.route('/remittance_payments/remittance_payments/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/remittance_payments/remittance_payments/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('remittance_payments.listing', {
#             'root': '/remittance_payments/remittance_payments',
#             'objects': http.request.env['remittance_payments.remittance_payments'].search([]),
#         })

#     @http.route('/remittance_payments/remittance_payments/objects/<model("remittance_payments.remittance_payments"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('remittance_payments.object', {
#             'object': obj
#         })

# -*- coding: utf-8 -*-
# from odoo import http


# class PaymentReceiptCustom(http.Controller):
#     @http.route('/payment_receipt_custom/payment_receipt_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payment_receipt_custom/payment_receipt_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('payment_receipt_custom.listing', {
#             'root': '/payment_receipt_custom/payment_receipt_custom',
#             'objects': http.request.env['payment_receipt_custom.payment_receipt_custom'].search([]),
#         })

#     @http.route('/payment_receipt_custom/payment_receipt_custom/objects/<model("payment_receipt_custom.payment_receipt_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payment_receipt_custom.object', {
#             'object': obj
#         })

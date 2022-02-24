# -*- coding: utf-8 -*-
# from odoo import http


# class AccountingReports(http.Controller):
#     @http.route('/accounting_reports/accounting_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/accounting_reports/accounting_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('accounting_reports.listing', {
#             'root': '/accounting_reports/accounting_reports',
#             'objects': http.request.env['accounting_reports.accounting_reports'].search([]),
#         })

#     @http.route('/accounting_reports/accounting_reports/objects/<model("accounting_reports.accounting_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('accounting_reports.object', {
#             'object': obj
#         })

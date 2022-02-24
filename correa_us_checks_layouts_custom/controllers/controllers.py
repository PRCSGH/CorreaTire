# -*- coding: utf-8 -*-
# from odoo import http


# class CorreaUsChecksLayoutsCustom(http.Controller):
#     @http.route('/correa_us_checks_layouts_custom/correa_us_checks_layouts_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/correa_us_checks_layouts_custom/correa_us_checks_layouts_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('correa_us_checks_layouts_custom.listing', {
#             'root': '/correa_us_checks_layouts_custom/correa_us_checks_layouts_custom',
#             'objects': http.request.env['correa_us_checks_layouts_custom.correa_us_checks_layouts_custom'].search([]),
#         })

#     @http.route('/correa_us_checks_layouts_custom/correa_us_checks_layouts_custom/objects/<model("correa_us_checks_layouts_custom.correa_us_checks_layouts_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('correa_us_checks_layouts_custom.object', {
#             'object': obj
#         })

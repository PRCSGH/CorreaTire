# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class correa_us_checks_layouts_custom(models.Model):
#     _name = 'correa_us_checks_layouts_custom.correa_us_checks_layouts_custom'
#     _description = 'correa_us_checks_layouts_custom.correa_us_checks_layouts_custom'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

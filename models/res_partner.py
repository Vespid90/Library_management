from odoo import models, fields, api

class Partner(models.Model):
    _inherit ='res.partner'

    is_member = fields.Boolean(string="Is member")

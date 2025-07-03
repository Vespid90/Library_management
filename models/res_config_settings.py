from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    return_duration_due = fields.Integer(string="Return duration due",
                                         config_parameter='library_loan.return_duration_due')

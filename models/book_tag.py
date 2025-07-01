from odoo import models, fields


class BookTag(models.Model):
    _name = 'book.tag'
    _description = 'Book tag'
    _order = 'sequence,id'

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string="Tag")
    color = fields.Integer(string="Color")
    sequence = fields.Integer(default=10)

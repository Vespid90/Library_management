from odoo import models, fields, api

class BookCategory(models.Model):
    _name = 'book.category'
    _description = 'Book category'

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Category')
    description = fields.Char(string='Description')
    book_ids = fields.Many2many(comodel_name='library.book', string='Book name')
    total_books= fields.Integer(string="Total book(s)", compute='_compute_total_books')
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('name_code_unique', 'unique (name)', 'The name must be unique'),
    ]

    @api.depends('book_ids')
    def _compute_total_books(self):
        for record in self:
            record.total_books = len(record.book_ids)

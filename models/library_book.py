from odoo import models, fields, api
from odoo.exceptions import ValidationError



class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library book'
    _order = 'name asc'

    active = fields.Boolean(string='Active')
    name = fields.Char(string="Book's name")
    author = fields.Char(string='Author')
    limited_age = fields.Integer(string="Age limited")
    publication_date = fields.Date(string='Publication Date', required=True)
    summary = fields.Char(string="Summary")
    pages = fields.Integer(string="Pages")
    isbn = fields.Char(string="Reference number", help='International Standard Book Number')
    color = fields.Integer(string="Color")
    state = fields.Selection([("available", "Available"), ("borrowed", "Borrowed"), ("lost", "Lost")], string="Statut")
    quantity = fields.Integer(string="Quantity")
    cover = fields.Binary(string='Cover')
    price = fields.Float(string="Price", digits=(16, 4))
    member_ids = fields.Many2many(comodel_name="library.member", string="Member")
    tag_ids = fields.Many2many(comodel_name="book.tag", string="Tag")
    favorite_member_ids = fields.One2many(comodel_name="library.member", inverse_name="favorite_book_id",
                                          string="Member's favorite book")
    category_ids = fields.Many2many(comodel_name='book.category', string='Category ID')
    image = fields.Binary(string="Image")
    sequence = fields.Integer(default=10)
    # date_today = fields.Date.today()


    def check_quantity(self):
        if self.quantity == 0:
            self.state = "borrowed"
        elif self.quantity < 0:
            self.state = "lost"
        else:
            self.state = "available"

    @api.onchange('quantity')
    def _onchange_state(self):
        """

        onchange fait un changement VISUEL lors de la creation d'abonnements

        """
        self.check_quantity()

    def button_book_up(self):
        self.quantity += 1
        self.check_quantity()

    @api.constrains('publication_date')
    def _check_publication_date(self):
        for record in self:
            if record.publication_date > fields.Date.today():
                raise ValidationError(
                    'Publication date is on the futur')

from odoo import models, fields, api

class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library member'

    @api.model
    def get_default_member_number(self):
        last_member = self.search([], order="member_number desc", limit=1)
        # last_member = self.search([])[-1]
        return last_member.member_number +1

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string="Name")
    mail = fields.Char(string="Mail")
    phone = fields.Integer(string="Phone")
    birthday_date = fields.Date(string="Birthday date")
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    member_number = fields.Integer(string="Member number", default=get_default_member_number)
    subscription_date = fields.Date(string="Subscription date")
    favorite_book_id = fields.Many2one(comodel_name="library.book", string="Favorite book")
    loan_ids = fields.One2many(comodel_name='library.loan', inverse_name='member_id', string='Loan ID', domain=[('state', '=', 'ongoing')])
    loan_count = fields.Integer(string="Numbers of loans by member", compute='_compute_loan_count')
    color = fields.Integer(string="Color")

    @api.depends('loan_ids')
    def _compute_loan_count(self):
        for record in self:
            record.loan_count = len(record.loan_ids)

    def action_loan_count(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "library.loan",
            "domain": [('member_id', '=', self.id)],
            "name": "loan_count",
            'view_mode': 'list,form',
        }

    @api.depends('birthday_date')
    def _compute_age(self):
        for record in self:
            if record.birthday_date:
                start = record.birthday_date
                now = fields.Date.today()
                delta = now - start
                print(delta)
                self.age = (delta.days / 365)
                print(self.age)
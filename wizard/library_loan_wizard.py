from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class LibraryLoanWizard(models.TransientModel):
    _name = 'library.loan.wizard'
    _description = 'Create Menu Wizard'

    member_id = fields.Many2one(comodel_name='library.member', string='Member ID')
    check_out_date = fields.Date(string="Check out date")
    return_date_due = fields.Date(string="Return date due")
    loan_books_ids = fields.Many2many(comodel_name='library.book', string='Books loans',
                                      domain=[('state', '=', 'available')])
    state = fields.Selection([("member", "Member"), ("list_book", "Book list"), ("preview", "Preview")],
                             string="Statut", default="member", required=True)

    def action_button_validation(self):
        for record in self:
            print(record.loan_books_ids.name)

    def action_create_record(self):
        for book in self.loan_books_ids:
            self.env['library.loan'].create({
                'book_id': book.id,
                'check_out_date': self.check_out_date,
                'return_date_due': self.return_date_due,
                'member_id': self.member_id.id,
                'state':'ongoing'
            })


    def action_list_book(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "library.loan.wizard",
            "name": "Book list",
            'view_mode': 'form',
            'context': {
                "default_state":'list_book',
                'default_member_id': self.member_id.id,
                'default_return_date_due': self.return_date_due,
                'default_loan_books_ids': self.loan_books_ids.ids,
            },
            'target': 'new',
        }

    def action_preview_book(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "library.loan.wizard",
            "name": "Preview",
            'view_mode': 'form',
            'context': {
                "default_state": 'preview',
                'default_member_id': self.member_id.id,
                'default_return_date_due': self.return_date_due,
                'default_loan_books_ids': self.loan_books_ids.ids,
            },
            'target': 'new',
        }

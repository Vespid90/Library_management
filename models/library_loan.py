from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Library loan'
    _inherit = 'mail.thread'

    name = fields.Char(string="Name", readonly=True, copy=False)
    active = fields.Boolean(string="Active", default=True)
    check_out_date = fields.Date(string="Check out date")
    return_date_due = fields.Date(string="Return date due")
    return_date_effective = fields.Date(string="Return date effective")
    state = fields.Selection([("ongoing", "Ongoing"), ("returned", "Returned"), ("late", "Late")], string="State",
                             tracking=True)
    member_id = fields.Many2one(comodel_name='library.member', string='Member ID', required=True)
    book_id = fields.Many2one(comodel_name='library.book', string='Book name', required=True)
    date_today = fields.Date.today()

    book_ids_domains = fields.Many2many(comodel_name='library.book', compute="_compute_book_name", store=True)

    @api.model_create_multi
    def create(self, vals_list):
        """

        méthode create pour enregistrer les abonnements dans la db

        """
        for vals in vals_list:
            if not vals.get('book_id'):
                raise ValidationError("Veuillez sélectionner un livre")

        results = super().create(vals_list)

        for rec in results:
            if rec.book_id.quantity <= 0:
                raise ValidationError("Le livre n'est plus disponible")
            rec.book_id.quantity -= 1

            rec.name = f"{self.env['ir.sequence'].next_by_code('library.loan')} {rec.book_id.name} loan by {rec.member_id.name}"

        return results

    def write(self, vals):
        """

        méthode write pour enregistrer les éditions d'abonnements dans la db

        """
        if vals.get('state') == "returned":
            for record in self:
                record.active = False
                record.book_id.quantity += 1
        # if vals.get('active') == True:
        #     sequences = self.env['ir.sequence'].search([('name', '=like', 'Library loan sequence' )])
        #     sequences.write({'number_next_actual': 1})
        #     print(sequences)
        return super().write(vals)

    def _message_cron(self):
        for record in self.search([]):
            if record.return_date_effective == False and record.date_today > record.return_date_due:
                record.message_post(
                    body=f"La date de retour du livre était le {record.return_date_due}, il a donc {record.date_today - record.return_date_due} jours de retard")

    def _action_share_book(self):
        for record in self:
            book_info = f"Nom du livre: {record.book_id.name}, Date de l'emprunt: {record.check_out_date}, Date de retour présumé: {record.return_date_due}"
            record.message_post(body=book_info)

    @api.model
    def default_get(self, fields_list):
        result = super().default_get(fields_list)
        if 'check_out_date' in fields_list and 'return_date_due' in fields_list:
            result['check_out_date'] = fields.Date.today()
            result['return_date_due'] = fields.Date.today() + relativedelta(days=int(self.env['ir.config_parameter'].get_param('library_loan.return_duration_due')))
            #le get_param donne TOUJOURS un string, il faut donc forcer le typage INTEGER ici
        return result

    @api.depends('')
    def action_library_loan_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "library.loan.wizard",
            # "domain": [('', '=', '')],
            "name": "Nom du membre",
            'view_mode': 'form',
            'context': {
                'default_member_id': self.member_id.id,
                'default_return_date_due': self.return_date_due,
            },
            'target': 'new',
        }

    @api.depends('member_id')
    def _compute_book_name(self):
        for rec in self:
            print("member age:", rec.member_id.age)
            if rec.member_id:
                rec.book_ids_domains = self.env['library.book'].search([('limited_age','<=',rec.member_id.age)])
            else:
                rec.book_ids_domains = self.env['library.book'].search([])


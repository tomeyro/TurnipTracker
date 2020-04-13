from odoo import models, fields, api, _


class TurnipPrice(models.Model):
    _name = 'turnip.price'
    _description = 'Turnip Price'
    _sorted = 'date DESC, time DESC'

    island_id = fields.Many2one('turnip.island', 'Turnip Island', required=True)
    date = fields.Date(string='Price Date', required=True)
    time = fields.Selection([
        ('am', 'A.M.'),
        ('pm', 'P.M.'),
    ], string='Price Time', required=True)
    price = fields.Integer(required=True)
    comment = fields.Char()

    _sql_constraints = [
        ('unique_price_per_datetime', 'UNIQUE(island_id, date, time)',
         _('You already assigned the price for this particular date and time.')),
    ]

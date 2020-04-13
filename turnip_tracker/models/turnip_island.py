from datetime import datetime, timedelta
from odoo import models, fields, api, _


class TurnipIsland(models.Model):
    _name = 'turnip.island'
    _description = 'Turnip Island'

    owner_id = fields.Many2one('res.users', string='Owner User')

    name = fields.Char("Island's Name", required=True)
    villager = fields.Char("Villager's Name", required=True)

    hemisphere = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
    ], default='north', required=True)
    timezone = fields.Selection([
        ('-12', '-12'), ('-11', '-11'), ('-10', '-10'), ('-9', '-9'), ('-8', '-8'),
        ('-7', '-7'), ('-6', '-6'), ('-5', '-5'), ('-4', '-4'), ('-3', '-3'),
        ('-2', '-2'), ('-1', '-1'), ('0', '0'), ('+1', '+1'), ('+2', '+2'),
        ('+3', '+3'), ('+4', '+4'), ('+5', '+5'), ('+6', '+6'), ('+7', '+7'),
        ('+8', '+8'), ('+9', '+9'), ('+10', '+10'), ('+11', '+11'), ('+12', '+12'),
        ('+13', '+13'), ('+14', '+14'),
    ], default='0', required=True)

    comment = fields.Text()

    twitter = fields.Char()
    reddit = fields.Char()
    nintendo = fields.Char()

    price_ids = fields.One2many('turnip.price', 'island_id', string='Turnip Prices')

    is_online = fields.Boolean(default=False)
    online_until = fields.Datetime()

    @api.multi
    def set_online(self):
        half_hour = datetime.now() + timedelta(minutes=30)
        for record in self:
            record.is_online = True
            record.online_until = half_hour

    @api.multi
    def set_offline(self):
        for record in self:
            record.is_online = False
            record.online_until = False

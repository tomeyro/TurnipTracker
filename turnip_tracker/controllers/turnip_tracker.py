from odoo.http import request, route, Controller
from odoo.addons.portal.controllers.portal import pager


class TurnipTrackerController(Controller):

    @route(['/turnip_tracker', '/turnip_tracker/page/<int:page>'], type='json', auth="public", website=True)
    def turnip_tracker(self, page=False, **kw):
        values = {}
        per_page = kw.get('per_page', 100)

        price_model = request.env['turnip.price']

        filters = {}
        for field in ['island', 'villager', 'date', 'time', 'price']:
            filters[field] = kw.get(field) or False

        domain = [
            ('date', '!=', False) if not filters.get('date') else ('date', '=', filters.get('date')),
            ('price', '>', filters.get('price') or 0),
            ('time', '!=', False) if not filters.get('time') else ('time', '=', filters.get('time')),
            ('island_id.name', '=ilike', filters.get('island')) if filters.get('island') else ('island_id.name', '!=', False),
            ('island_id.villager', '=ilike', filters.get('villager')) if filters.get('villager') else ('island_id.villager', '!=', False),
        ]

        count = price_model.search_count(domain)
        portal_pager = pager(url="/my/islands", total=count, page=page, step=per_page)

        prices = price_model.search(domain)

        price_fields = price_model.fields_get()
        times = dict(price_fields['time']['selection'])

        values.update({
            'prices': prices,
            'times': times,
            'filters': filters,
        })

        return request.website.viewref('turnip_tracker.turnip_tracker_widget').render(values)

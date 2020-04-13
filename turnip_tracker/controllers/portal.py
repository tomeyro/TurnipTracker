from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal, pager


class CustomerPortalExtension(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortalExtension, self)._prepare_portal_layout_values()
        island_count = request.env['turnip.island'].search_count([
            ('owner_id', '=', request.env.user.id),
        ])
        values.update({
            'island_count': island_count,
        })
        return values

    @route(['/my/islands', '/my/islands/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_islands(self, page=1, **kw):
        values = {}
        user = request.env.user
        island_model = request.env['turnip.island']

        domain = [
            ('owner_id', '=', user.id),
        ]

        # count for pager
        count = island_model.search_count(domain)

        # make pager
        portal_pager = pager(url="/my/islands", total=count, page=page, step=self._items_per_page)

        # search the count to display, according to the pager data
        islands = island_model.search(domain, order='id', limit=self._items_per_page, offset=portal_pager['offset'])

        hemispheres = dict(island_model.fields_get()['hemisphere']['selection'])

        values.update({
            'islands': islands,
            'pager': portal_pager,
            'hemispheres': hemispheres,
        })
        return request.render("turnip_tracker.turnip_portal_island", values)

    @route([
            '/my/islands/new',
            '/my/islands/<int:island_id>',
    ], type='http', methods=['POST'], auth="user", website=True, sitemap=False)
    def portal_my_islands_form(self, island_id=False, **kw):
        values = {}
        errors = {}

        island_model = request.env['turnip.island']
        user = request.env.user

        island = False
        if island_id:
            island = island_model.browse(int(island_id))

        if island and island.owner_id != user:
            return request.redirect('/my/islands')

        submitted = 'submitted' in kw
        required = ['name', 'villager', 'hemisphere', 'timezone', 'owner_id']
        fields = required + ['twitter', 'reddit', 'nintendo', 'comment']

        for field in fields:
            values[field] = kw.get(field, island[field] if island else '') or False
            if field.endswith('_id'):
                values[field] = int(values[field] or 0)
            if submitted and not values[field] and field in required:
                errors[field] = True

        if submitted and not errors:
            if island:
                island.write(values)
                return request.redirect('/my/islands')
            island_model.create(values)
            return request.redirect('/my/islands')

        island_fields = island_model.fields_get()
        hemispheres = island_fields['hemisphere']['selection']
        timezones = island_fields['timezone']['selection']

        return request.render("turnip_tracker.turnip_portal_island_form", {
            'user': request.env.user,
            'island': island,
            'form': values,
            'errors': errors,
            'hemispheres': hemispheres,
            'timezones': timezones,
        })

    @route([
            '/my/islands/<int:island_id>/toggle_online'
    ], type='http', methods=['POST'], auth="user", website=True, sitemap=False)
    def portal_my_islands_toggle_online(self, island_id, **kw):
        island = request.env['turnip.island'].browse(int(island_id))

        if not island or island.owner_id != request.env.user:
            return request.redirect('/my/islands')

        if not island.is_online or 'refresh_online' in kw:
            island.set_online()
        else:
            island.set_offline()
        return request.redirect('/my/islands')

    @route([
            '/my/islands/<int:island_id>/prices',
            '/my/islands/<int:island_id>/prices/page/<int:page>',
    ], type='http', auth="user", website=True)
    def portal_my_islands_prices(self, island_id, page=1, **kw):
        values = {}
        user = request.env.user
        island_model = request.env['turnip.island']

        island = request.env['turnip.island'].browse(int(island_id))

        if not island or island.owner_id != request.env.user:
            return request.redirect('/my/islands')

        domain = [
            ('island_id', '=', island.id),
        ]

        price_model = request.env['turnip.price']

        # count for pager
        count = price_model.search_count(domain)

        # make pager
        portal_pager = pager(
            url="/my/islands/%s/prices" % island.id, total=count, page=page, step=self._items_per_page)

        # search the count to display, according to the pager data
        prices = price_model.search(
            domain, order='date DESC, time DESC', limit=self._items_per_page, offset=portal_pager['offset'])

        price_fields = price_model.fields_get()
        times = dict(price_fields['time']['selection'])

        values.update({
            'island': island,
            'pager': portal_pager,
            'prices': prices,
            'times': times,
        })
        return request.render("turnip_tracker.turnip_portal_island_prices", values)

    @route([
            '/my/islands/<int:island_id>/prices/new'
    ], type='http', methods=['POST'], auth="user", website=True, sitemap=False)
    def portal_my_islands_prices_new(self, island_id, **kw):
        user = request.env.user
        island_model = request.env['turnip.island']

        island = request.env['turnip.island'].browse(int(island_id))

        if not island or island.owner_id != request.env.user:
            return request.redirect('/my/islands')

        date = kw.get('date')
        time = kw.get('time')
        price_amount = abs(int(kw.get('price') or 0))
        comment = kw.get('comment') or False

        if not date or not time or not price_amount:
            return request.redirect('/my/islands/%s/prices' % island.id)

        price_model = request.env['turnip.price']

        price = price_model.search([
            ('date', '=', date),
            ('time', '=', time),
            ('island_id', '=', island.id),
        ])
        if price:
            price.write({'price': price_amount, 'comment': comment})
            return request.redirect('/my/islands/%s/prices' % island.id)

        price = price_model.create({
            'date': date,
            'time': time,
            'price': price_amount,
            'island_id': island.id,
            'comment': comment,
        })
        return request.redirect('/my/islands/%s/prices' % island.id)

    @route([
            '/my/islands/<int:island_id>/prices/<int:price_id>/delete'
    ], type='http', methods=['POST'], auth="user", website=True, sitemap=False)
    def portal_my_islands_prices_delete(self, island_id, price_id, **kw):
        ser = request.env.user
        island_model = request.env['turnip.island']

        island = request.env['turnip.island'].browse(int(island_id))

        if not island or island.owner_id != request.env.user:
            return request.redirect('/my/islands')

        price_model = request.env['turnip.price']
        price = price_model.search([
            ('island_id', '=', island.id),
            ('id', '=', price_id),
        ])
        if price:
            price.unlink()
        return request.redirect('/my/islands/%s/prices' % island.id)

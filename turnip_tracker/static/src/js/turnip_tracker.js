odoo.define('turnip_tracker.widgets', function (require) {
    'use strict';

    var animation = require('website.content.snippets.animation');
    var _t = require('web.core')._t;

    function getUrlParameter (sParam) {
        var sPageURL = window.location.search.substring(1),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;
        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
            }
        }
    }

    animation.registry.turnip_tracker_widget = animation.Class.extend({
        selector: 'turnip_tracker',

        start: function () {
            var self = this;

            var params = {
                'island': getUrlParameter('island'),
                'villager': getUrlParameter('villager'),
                'date': getUrlParameter('date'),
                'time': getUrlParameter('time'),
                'price': getUrlParameter('price'),
            }

            var def = $.Deferred();
            this._rpc({
                route: '/turnip_tracker',
                params: params,
            }).then(function (html) {
                const $html = $(html);
                self.$target.empty();
                self.$target.html($html);

                self.register_events();
            }, function () {
                self.$target.empty();
                self.$target.html($('<p/>', {
                    class: 'text-danger text-center mt16 mb16',
                    text: _t("An error occurred while loading the turnip tracker widget. " +
                             "If the problem persists please contact the administrator."),
                }));
            }).always(def.resolve.bind(def));

            return $.when(this._super.apply(this, arguments), def);
        },

        register_events: function () {
            const self = this;
            const carriers = self.$('#delivery_carriers_list')
                .find('.delivery_carrier');
            carriers.on('change', function () {
                $('#o_payment_form_pay')
                    .addClass('disabled').attr('disabled', 'disabled');
                self.$('#delivery_carriers_form').submit();
            });
        },

        destroy: function () {
            this.$target.empty();
            this._super.apply(this, arguments);
        },
    });
});

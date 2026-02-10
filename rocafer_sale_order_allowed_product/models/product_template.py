# Copyright 2024 Xtendoo - Salvador González

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None):
        partner_id = self.env.context.get("restricted_partner_id")
        if partner_id:
            domain = list(domain) + [("res_partner_id", "=", partner_id)]
        return super()._search(
            domain,
            offset=offset,
            limit=limit,
            order=order,
        )

from odoo import models, api, fields


class StockMove(models.Model):
    _inherit = "stock.move"

    total_units = fields.Integer(
        string="Unidades totales",
        compute="_compute_total_units",
        store=True,
        readonly=False,
    )

    @api.depends("product_uom_qty", "product_uom")
    def _compute_total_units(self):
        for line in self:
            if line.product_uom:
                line.total_units = line.product_uom_qty * line.product_uom.factor_inv
            else:
                line.total_units = 0

    @api.onchange("total_units")
    def onchange_total_units(self):
        for line in self:
            if line.total_units and line.product_uom:
                line.product_uom_qty = line.total_units / line.product_uom.factor_inv
                line._compute_product_qty()

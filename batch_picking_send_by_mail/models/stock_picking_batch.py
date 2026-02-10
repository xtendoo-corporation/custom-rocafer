from odoo import _, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    def action_picking_batch_send(self):
        self.ensure_one()
        template = self.company_id.stock_mail_confirmation_template_id
        compose_form = self.env.ref(
            "mail.email_compose_message_wizard_form",
            False,
        )
        ctx = dict(
            default_model="stock.picking.batch",
            default_res_ids=[self.id],
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode="comment",
            user_id=self.env.user.id,
        )
        return {
            "name": _("Compose Email"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form.id, "form")],
            "view_id": compose_form.id,
            "target": "new",
            "context": ctx,
        }

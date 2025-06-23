from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class StudioApprovalRule(models.Model):
    _inherit = "studio.approval.rule"

    @api.depends("group_id")
    @api.depends_context("uid")
    def _compute_can_validate(self):
        _logger.info(f"StudioApprovalRule _compute_can_validate | Context: {self.env.context}")

        active_id = self.env.context.get('active_id')
        _logger.info(f"StudioApprovalRule active_id | Context active_id: {active_id}")
        group_xmlids = self.group_id.get_external_id()
        for rule in self:
            rule.can_validate = False
            if active_id and rule.model_name == 'sale.order' and not self.env.user.has_group(group_xmlids[rule.group_id.id]):
                sale_order = self.env[rule.model_name].browse(active_id)
                if sale_order:
                    approver_ids = [
                        sale_order.partner_shipping_id.user_id.id,
                        sale_order.partner_id.user_id.id,
                        sale_order.partner_invoice_id.user_id.id,
                    ]
                    if self.env.user.id in approver_ids:
                        rule.can_validate = True
                    else:
                        if group_xmlids:
                            rule.can_validate = self.env.user.has_group(group_xmlids[rule.group_id.id])
            else:
                if group_xmlids:
                    rule.can_validate = self.env.user.has_group(group_xmlids[rule.group_id.id])
            _logger.info(f"StudioApprovalRule active_id | Context active_id: {rule.can_validate}")

    def set_approval(self, res_id, approved):
        self.ensure_one()
        _logger.info(f"set_approval set_approval | Context active_id approved: {res_id, approved}")
        _logger.info(f"set_approval set_approval  set_approval | Context : {self.env.context}")
        entry = self.with_context(active_id=res_id)._set_approval(res_id, approved)
        return entry and entry.approved
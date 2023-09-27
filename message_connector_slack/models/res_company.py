# Copyright 2022 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    slack_log_channel_test = fields.Many2one(
        comodel_name="message.connector.channel",
        string="Test Channel Test"
    )
    slack_token_test = fields.Char(
        string="Slack Token Test"
    )
    slack_log_channel_production = fields.Many2one(
        comodel_name="message.connector.channel",
        string="Test Channel Production"
    )
    slack_token_production = fields.Char(
        string="Slack Token Production"
    )
    slack_active = fields.Boolean(
        string="Active Slack",
        default=False
    )
    slack_token = fields.Char(
        string="Slack Token",
        compute="_compute_slack_token",
        store=True
    )
    slack_active_production = fields.Boolean(
        string="Test / Production Environment",
        default=False
    )
    slack_log_msg_deletion_freq = fields.Integer(
        string="Frequency of Deletion of Slack Messages from the Log (days)",
        default=0
    )

    def get_message_services(self):
        res = super().get_message_services()
        res.append(('slack', 'Slack'))
        return res

    @api.depends(
        'slack_active_production',
        'slack_token_production',
        'slack_token_test',
        'slack_active'
    )
    def _compute_slack_token(self):
        for sel in self:
            res = sel.slack_token_test
            if sel.slack_active_production:
                res = sel.slack_token_production
            sel.slack_token = res

# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    slack_log_channel_test = fields.Many2one(
        comodel_name="message.connector.channel",
        string="Test Channel Test",
        related="company_id.slack_log_channel_test",
        store=True,
        readonly=False,
        domain=lambda self: "[\
            ('messaging_service', '=', 'slack'),\
            ('state', '=', 'validated')\
        ]"
    )
    slack_token_test = fields.Char(
        string="Slack Token Test",
        related="company_id.slack_token_test",
        store=True,
        readonly=False
    )
    slack_log_channel_production = fields.Many2one(
        comodel_name="message.connector.channel",
        string="Slack Test Channel Production",
        related="company_id.slack_log_channel_test",
        store=True,
        readonly=False
    )
    slack_token_production = fields.Char(
        string="Slack Token Production",
        related="company_id.slack_token_production",
        store=True,
        readonly=False
    )
    slack_active = fields.Boolean(
        related="company_id.slack_active",
        store=True,
        readonly=False,
        string="Active Slack"
    )
    slack_active_production = fields.Boolean(
        related="company_id.slack_active_production",
        store=True,
        readonly=False,
        string="Test / Production Environment"
    )
    slack_log_msg_deletion_freq = fields.Integer(
        related="company_id.slack_log_msg_deletion_freq",
        default=0,
        store=True,
        readonly=False,
        help="If set to zero, messages will be deleted at the general "
        "frequency. Any other value greater than zero will cause slack "
        "messages to be deleted at this frequency.",
        string="Frequency of Deletion of Slack Messages from the Log (days)"
    )

    def set_values(self):
        """ Deactivates Slack if Message Connector Base is disabled
            Sets all Slack messages to draft status 
        """
        res = super(ResConfigSettings, self).set_values()
        if not self.message_connector_active:
            self.slack_active = False
        elif self.message_connector_active and not self.slack_active:
            self.env['message.connector.channel'].search([
                    ('state', '=', 'validated'),
                    ('messaging_service', '=', 'slack')
            ]).write({'state': 'draft'})
            self.env['message.connector.message.builder'].search([
                    ('state', '=', 'active'),
                    ('messaging_service', '=', 'slack')
            ]).write({'state': 'draft'})
        return res

    @api.constrains('slack_log_msg_deletion_freq')
    def _check_log_msg_deletion_freq(self):
        """ Checks that the deletion frequency is equal to or 
            greater than zero.
        """
        for sel in self:
            if sel.log_msg_deletion_freq < 0:
                raise ValidationError(_(
                    "The frequency of slack message log "
                    "deletion must be greater than or equal to zero."
                ))

    def action_slack_test_message(self):
        return self._send_test_message('slack')
    
    def _get_test_message_vals(self, messaging_service=False): # XXX cambiar a get_tes
        vals = super()._get_test_message_vals(messaging_service)
        if messaging_service == 'slack':
            if self.slack_active_production:
                channel = self.slack_log_channel_production.slack_name
            else:
                channel = self.slack_log_channel_test.slack_name
            attachments = [{
                "title": 'This message is a test from Odoo',
                "color": "#36a64f",
                "text": "Test",
            }]
            vals.update({
                'channel': channel,
                'attachments': attachments,
                'msg': 'Test message',
                'attachments': attachments
            })
        return vals

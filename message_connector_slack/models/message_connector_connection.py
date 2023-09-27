# Copyright 2023 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from slack import WebClient
import datetime
from odoo.tools.safe_eval import safe_eval


class MessageConnectorConnection(models.Model):
    _inherit = 'message.connector.connection'

    attachments = fields.Text(
        string='Attachments',
    )
    msg = fields.Char(
        string="Message"
    )

    def _slack_send_message(self):
        for sel in self.filtered(lambda x: x.env.company.slack_active):
            state = "sent"
            error = ""
            api_response = {'error': 'Conection Error'}
            api_response_message = {}
            api_response_file = {}
            # Slack conection
            sc = WebClient(sel.env.company.slack_token)
            # Post message
            if sel.msg or sel.attachments != [{}]:
                try:
                    api_response_message = sc.chat_postMessage( 
                        channel=sel.channel, 
                        text=sel.msg if sel.msg else '', 
                        attachments=safe_eval(sel.attachments), 
                        username='Odoo'
                    )
                except Exception as e:
                    error = "{}".format(e)
                    state = "error"
                api_response = api_response_message
            # Upload File
            if not error and sel.add_report:
                try:
                    api_response_file = sc.files_upload(
                        channels=sel.channel,
                        file=sel._decode_data_file(sel.data_file),
                        initial_comment=sel.message_report
                    )
                except Exception as e:
                    error = "{}".format(e)
                    state = "error"
                api_response = "{}\n{}".format(
                    api_response_message, api_response_file
                )
            sel.write({
                'api_response': error if error else api_response,
                'state': state,
                'error': error
            })

    @api.autovacuum
    def _gc_messages(self):
        slack_days = self.env.company.slack_log_msg_deletion_freq
        general_days = self.env.company.slack_log_msg_deletion_freq
        if slack_days:
            slack_timeout = datetime.datetime.utcnow()-datetime.timedelta(
                days=slack_days
            )
            self.search([
                ('date', '<', slack_timeout),
                ('messaging_service', '=', 'slack')
            ]).unlink()
            general_timeout = datetime.datetime.utcnow()-datetime.timedelta(
                days=general_days
            )
            self.search([
                ('date', '<', general_timeout),
                ('messaging_service', '!=', 'slack')
            ]).unlink()
        else:
            super()._gc_messages()

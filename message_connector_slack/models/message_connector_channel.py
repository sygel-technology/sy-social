# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class MessageConnectorChannel(models.Model):
    _inherit = "message.connector.channel"

    slack_name = fields.Char(
        string="Slack Channel Name",
        required=True
    )

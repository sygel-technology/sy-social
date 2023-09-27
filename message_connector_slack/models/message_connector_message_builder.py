# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import ValidationError


class MessageConnectorMessageBuilder(models.Model):
    _inherit = "message.connector.message.builder"

    message_header = fields.Char(
        string="Message Header",
        states={
            "active": [("readonly", True)],
            "canceled": [("readonly", True)]
        },
        help="Optional field to add a text in the header"
    )
    add_record_name_header = fields.Boolean(
        string="Add Record Name in the Header",
        states={
            "active": [("readonly", True)],
            "canceled": [("readonly", True)]
        },
        help="Insert the name of the record in the header. "
        "Format: message_header + record_name"
    )
    bold_header = fields.Boolean(
        string="Header in Bold",
        states={
            "active": [("readonly", True)],
            "canceled": [("readonly", True)]
        },
        default=True,
        help="To format the header in boldface type"
    )
    title = fields.Char(
        string='Title',
        states={
            "active": [("readonly", True)],
            "canceled": [("readonly", True)]
        },
        help="To add a title in the attachment"
    )
    add_record_name_title = fields.Boolean(
        string="Add Record Name in the Title",
        states={
            "active": [("readonly", True)],
            "canceled": [("readonly", True)]
        },
        help="Insert the name of the record in the title. "
        "Format: title + record_name"
    )
    text = fields.Char(
        string="Subtitle",
        states={
            "active": [("readonly", True)],
            "canceled": [("readonly", True)]
        },
        help="To add a subtitle in the attachment"
    )
    add_record_name_subtitle = fields.Boolean(
        string="Add Record Name in the Subtitle",
        states={
            "active": [("readonly", True)],
            "canceled": [("readonly", True)]
        },
        help="Insert the name of the record in the subtitle. "
        "Format: subtitle + record_name"
    )
    color = fields.Char(
        string="Color",
        states={
            "active": [("readonly", True)],
            "canceled": [("readonly", True)]
        },
        default="#FFFFFF",
        help="To change de line color of the attachment"
    )
    attachment = fields.Text(
        string="Attachment",
        states={
            "active": [("readonly", True)],
            "canceled": [("readonly", True)]
        },
    )
    prefix_button_name = fields.Char(
        string="Prefix button name",
        states={
            "active": [("readonly", True)],
            "canceled": [("readonly", True)]
        },
        help="The button name will be prefix + field_id + sufix."
        "The fields prefix, field_button_id and suffix are all optional."
    )
    field_button_id = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Field Button Name",
        help="The button name will be prefix + field_id + sufix."
        "The fields prefix, field_button_id and suffix are all optional.",
        states={
            "active": [("readonly", True)],
            "canceled": [("readonly", True)]
        },
        domain="[('model_id', '=', model_id)]",
        ondelete="cascade"
    )
    suffix_button_name = fields.Char(
        string="Suffix Button Name",
        help="The button name will be prefix + field_id + sufix."
        "The fields prefix, field_button_id and suffix are all optional.",
        states={
            "active": [("readonly", True)],
            "canceled": [("readonly", True)]
        }
    )
    text_fallback = fields.Char(
        string="Text fallback",
        states={
            "active": [("readonly", True)],
            "canceled": [("readonly", True)]
        }
    )
    add_button_action = fields.Boolean(
        string="Add action button",
        help="Add a button to navigate directly to the "
        "record_id from the chat",
        states={
            "active": [("readonly", True)],
            "canceled": [("readonly", True)]
        },
        default=True
    )

    def _get_title(self, record_id, attachment):
        self.ensure_one()
        title = self.title
        if self.add_record_name_title:
            title = "{} {}".format(title, record_id.name)
        if title:
            attachment['title'] = title
        return attachment

    def _get_subtitle(self, record_id, attachment):
        self.ensure_one()
        subtitle = self.text
        if self.add_record_name_subtitle:
            subtitle += " {}".format(record_id.name)
        if subtitle:
            attachment['text'] = subtitle
        return attachment

    def _get_button_name(self, record_id):
        self.ensure_one()
        res = ""
        field = ""
        if self.field_button_id:
            field = safe_eval(
                "self.{}".format(self.field_button_id.name),
                {"self": record_id}
            )
        var = [self.prefix_button_name, '{}'.format(field), self.suffix_button_name]
        res = " ".join(filter(None, var))
        return res

    def _get_fallback(self, record_id, attachment):
        self.ensure_one()
        if self.add_button_action:
            fallback = "{} {}".format(
                self._get_button_name(record_id),
                self._get_url(record_id)
            )
            attachment['fallback'] = fallback
        return attachment

    def _get_action(self, record_id, attachment):
        self.ensure_one()
        action = {}
        if self.add_button_action:
            action = {
                "type": "button",
                "text": self._get_button_name(record_id),
                "url": self._get_url(record_id)
            }
            attachment['actions'] = [action]
        return attachment

    def _get_attachments(self, record_id):
        self.ensure_one()
        attachment = {}
        attachment = self._get_title(record_id, attachment)
        attachment = self._get_subtitle(record_id, attachment)
        attachment = self._get_fallback(record_id, attachment)
        attachment = self._get_action(record_id, attachment)
        fields = self._get_fields(record_id)
        if fields:
            attachment['fields'] = fields
        if attachment:
            attachment['color'] = self.color
        return [attachment]

    def _get_header_message(self, record_id):
        self.ensure_one()
        res = ''
        var = [self.message_header]
        if self.add_record_name_header:
            var.append(record_id.name)
        res = " ".join(filter(None, var))
        if self.bold_header and res:
            res = "*{}*".format(res)
        return res

    def _get_message_vals(self, record_id):
        self.ensure_one()
        vals = super()._get_message_vals(record_id)
        if self.messaging_service == 'slack':
            attachments = self._get_attachments(record_id)
            message = self._get_header_message(record_id)
            vals.update({
                'msg': message,
                'attachments': attachments,
                'channel': self.channel_id.slack_name
            })
        return vals

    def _get_field_vals(self, field, value):
        res = super()._get_field_vals(field, value)
        if self.messaging_service == 'slack':
            res['short'] = field.short
        return res

    @api.constrains(
        'add_button_action',
        'prefix_button_name',
        'field_button_id',
        'suffix_button_name'
    )
    def _check_button_name_fields(self):
        """ Checks that if the add_button_name option is checked there is at 
            least one field to construct the button name.
        """
        for sel in self.filtered(lambda x: x.add_button_action):
            if not (self.prefix_button_name or
                    self.field_button_id or
                    self.suffix_button_name):
                raise ValidationError(_(
                    "For the button to be displayed in the message the button "
                    "name must contain some field."
                ))

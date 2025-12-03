# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_get_recipients_classify(
        self, message, recipients_data, model_description, msg_vals=None
    ):
        result = super()._notify_get_recipients_classify(
            message, recipients_data, model_description, msg_vals=msg_vals
        )
        technical_model_name = (
            msg_vals.get("model") if msg_vals and "model" in msg_vals else self._name
        )
        hidden_mail_models = self.env["ir.model"].get_hidden_mail_portal_access_models()

        for group in result:
            group["has_button_access"] = (
                technical_model_name not in hidden_mail_models
                and group.get("notification_group_name")
                in [
                    "customer",
                    "portal",
                    "portal_customer",
                ]
            )
        return result

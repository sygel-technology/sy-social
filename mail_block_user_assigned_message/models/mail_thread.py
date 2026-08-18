# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _message_auto_subscribe_notify(self, partner_ids, template):
        self = self.with_context(subscribe_notify=True)
        return super()._message_auto_subscribe_notify(partner_ids, template)

    def message_notify(
        self,
        *,
        body="",
        subject=False,
        author_id=None,
        email_from=None,
        model=False,
        res_id=False,
        subtype_xmlid=None,
        subtype_id=False,
        partner_ids=False,
        attachments=None,
        attachment_ids=None,
        **kwargs,
    ):
        if self and self.env.context.get("subscribe_notify") and partner_ids:
            partner_ids = (
                self.env["res.partner"]
                .search(
                    [
                        ("id", "in", partner_ids),
                        "|",
                        ("block_assigned_message", "=", False),
                        (
                            "block_assigned_message_model_ids",
                            "not in",
                            self.env["ir.model"]._get(self._name).id,
                        ),
                    ]
                )
                .ids
            )
        return super().message_notify(
            body=body,
            subject=subject,
            author_id=author_id,
            email_from=email_from,
            model=model,
            res_id=res_id,
            subtype_xmlid=subtype_xmlid,
            subtype_id=subtype_id,
            partner_ids=partner_ids,
            attachments=attachments,
            attachment_ids=attachment_ids,
            **kwargs,
        )

# Copyright 2020 Valentin Vinagre <valentin.vinagre@sygel.es>
# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class MailMail(models.Model):
    _inherit = "mail.mail"

    def _get_partners_exclude_cc(self, cc_internal, partners):
        self.ensure_one()
        partners_do_not_notify = self.env["res.partner"]
        if not cc_internal:
            group_internal = self.env.ref("base.group_user")
            partners_do_not_notify = (
                self.env["res.users"]
                .search(
                    [
                        ("active", "in", (True, False)),
                        ("partner_id", "in", partners.ids),
                    ]
                )
                .filtered(lambda x: group_internal in x.groups_id)
                .mapped("partner_id")
            )
        else:
            partners_do_not_notify = (
                self.env["res.users"]
                .search(
                    [
                        ("active", "in", (True, False)),
                        ("partner_id", "in", partners.ids),
                        ("show_in_cc", "=", False),
                    ]
                )
                .mapped("partner_id")
            )
        return partners_do_not_notify

    def _send(
        self,
        auto_commit=False,
        raise_exception=False,
        smtp_session=None,
        alias_domain_id=False,
    ):
        plain_text = """<div summary="o_mail_notification" style="padding: 0px;
 font-size: 10px;"><b>CC</b>: {}<hr style="background-color:rgb(204,204,204);
 border:medium none;clear:both;display:block;font-size:0px;min-height:1px;
 line-height:0; margin:4px 0 12px 0;"></div>
 """

        for mail in self.filtered(lambda a: a.model and a.res_id):
            obj = self.env[mail.model].browse(mail.res_id)
            if hasattr(obj, "message_follower_ids"):
                company = mail.env.user.company_id
                if hasattr(obj, "company_id") and obj.company_id:
                    company = obj.company_id
                accepted_model = mail.model not in company.cc_blocked_models.mapped(
                    "model"
                )
                if accepted_model:
                    partners = obj.message_follower_ids.mapped("partner_id")
                    cc_internal = company.show_internal_users_cc
                    partners_exclude_cc = mail._get_partners_exclude_cc(
                        cc_internal, partners
                    )
                    partners -= partners_exclude_cc
                    if len(partners) > 1:
                        # get names and emails
                        final_cc = None
                        mails = ""
                        for p in partners:
                            mails += f"{p.name} &lt;{p.email}&gt;, "
                        # join texts
                        final_cc = plain_text.format(mails[:-2])
                        # it is saved in the body_html field so that it does
                        # not appear in the odoo log
                        mail.body_html = final_cc + mail.body_html
        return super()._send(
            auto_commit=auto_commit,
            raise_exception=raise_exception,
            smtp_session=smtp_session,
            alias_domain_id=alias_domain_id,
        )

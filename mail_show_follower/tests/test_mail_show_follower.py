# Copyright 2024 Roger Sans <roger.sans@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging as logger

from odoo.tests import Form

from odoo.addons.mail.tests.common import MailCommon

_logger = logger.getLogger(__name__)


class TestMailShowFollower(MailCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model_used = cls.env["ir.model"]._get("res.partner")
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.partner_admin = cls.env.ref("base.partner_admin")
        cls.company_admin = cls.user_admin.company_id
        cls._test_email = "follower@test.example.com"
        cls.test_partner = cls.env["res.partner"].create(
            {
                "country_id": cls.env.ref("base.be").id,
                "email": cls._test_email,
                "mobile": "0456001122",
                "name": "Follower",
                "phone": "0456334455",
            }
        )

        cls.test_user_1 = cls.env["res.users"].create(
            {
                "name": "Demo_User1",
                "login": "desuser1",
                "show_in_cc": True,
                "email": "demouser1@test_mail.com",
            }
        )
        cls.test_user_2 = cls.env["res.users"].create(
            {
                "name": "Demo_User2",
                "login": "desuser2",
                "show_in_cc": True,
                "email": "demouser2@test_mail.com",
            }
        )

        # Add both users to followers of partner
        cls.test_partner.message_subscribe(
            partner_ids=[cls.test_user_1.partner_id.id, cls.test_user_2.partner_id.id]
        )

        # Create a email template
        cls.template = cls.env["mail.template"].create(
            {
                "lang": "{{ object.lang }}",
                "model_id": cls.model_used.id,
                "name": "Test template",
                "partner_to": "{{ object.id }}",
            }
        )

    def _bloqued_models_to_cc(self):
        # If model still not added into blocked models, add it.
        # If in models blocked, remove it.
        if self.model_used not in self.company_admin.cc_blocked_models:
            self.company_admin.cc_blocked_models = [(4, self.model_used.id)]
        else:
            self.company_admin.cc_blocked_models = [(3, self.model_used.id)]

    def _user_to_cc(self, user):
        # If user show in CC is checked, uncheck it. If not, check id
        user.show_in_cc = False if user.show_in_cc else True

    def _send_mail_with_cc(self):
        # Send an email with created template
        form = Form(
            self.env["mail.compose.message"].with_context(
                **{
                    "default_partner_ids": (self.test_partner).ids,
                    "default_model": self.test_partner._name,
                    "default_res_ids": self.test_partner.ids,
                    "default_template_id": self.template.id,
                    "default_subject": "Test mail",
                    "default_composition_mode": "mass_mail",
                    "body": "<p>Hello World</p>",
                }
            )
        )
        saved_form = form.save()

        with self.mock_mail_gateway():
            mail = saved_form._action_send_mail()

        return mail[0]["body_html"]

    def test_with_cc(self):
        # Check if partner have more than one follower.
        self.assertTrue(len(self.test_partner.message_follower_ids) > 1)

        # Check if Demo_User1 appears in mail
        mail_with_both_cc = self._send_mail_with_cc()
        self.assertTrue("Demo_User1" in mail_with_both_cc)

        # Uncheck show in CC option from Demo_User1 and
        # check if Demo_User1 appears in mail
        self._user_to_cc(self.test_user_1)
        mail_without_user_1 = self._send_mail_with_cc()
        self.assertFalse("Demo_User1" in mail_without_user_1)

        # Check show in CC option from Demo_User1 again and
        # check if Demo_User1 appears in mail
        self._user_to_cc(self.test_user_1)
        mail_with_user_1 = self._send_mail_with_cc()
        self.assertTrue("Demo_User1" in mail_with_user_1)

        # Add res.partner model to block models and
        # check if any user appears in mail
        self._bloqued_models_to_cc()
        mail_with_model_block = self._send_mail_with_cc()
        self.assertFalse(
            "Demo_User1" in mail_with_model_block
            or "Demo_User2" in mail_with_model_block
        )

        # Remove res.partner model from block models and
        # check if any user appears in mail
        self._bloqued_models_to_cc()
        mail_with_model_unblock = self._send_mail_with_cc()
        self.assertTrue(
            "Demo_User1" in mail_with_model_unblock
            or "Demo_User2" in mail_with_model_unblock
        )

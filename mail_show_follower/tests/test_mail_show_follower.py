# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form

from odoo.addons.mail.tests.common import MailCommon


class TestMailShowFollower(MailCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_main, cls.partner_follower = cls.env["res.partner"].create(
            [
                {"name": "Main Partner", "email": "partner_main@mail.com"},
                {"name": "Partner Follower", "email": "partner_follower@mail.com"},
            ]
        )
        cls.internal_user_1, cls.internal_user_2 = cls.env["res.users"].create(
            [
                {
                    "name": "Internal User 1",
                    "login": "internal_user_1@user.es",
                    "email": "internal_user_1@user.es",
                },
                {
                    "name": "Internal User 2",
                    "login": "internal_user_2@user.es",
                    "email": "internal_user_2@user.es",
                },
            ]
        )

        cls.partner_main_email = (
            f"{cls.partner_main.name} &lt;{cls.partner_main.email}&gt;"
        )
        cls.partner_follower_email = (
            f"{cls.partner_follower.name} &lt;{cls.partner_follower.email}&gt;"
        )
        cls.internal_user_1_email = (
            f"{cls.internal_user_1.name} &lt;{cls.internal_user_1.email}&gt;"
        )
        cls.internal_user_2_email = (
            f"{cls.internal_user_2.name} &lt;{cls.internal_user_2.email}&gt;"
        )

        cls.partner_main.message_subscribe(
            partner_ids=(
                cls.partner_follower
                + cls.partner_main
                + cls.internal_user_1.partner_id
                + cls.internal_user_2.partner_id
            ).ids
        )

    def send_email_cc(cls):
        form = Form(
            cls.env["mail.compose.message"].with_context(
                default_model=cls.partner_main._name,
                default_res_ids=[cls.partner_main.id],
            )
        )
        form.body = "<p>Test</p>"
        saved_form = form.save()
        with cls.mock_mail_gateway():
            saved_form._action_send_mail()

        return cls.partner_main.message_ids[0].mail_ids[0]

    def test_show_cc_contacts(self):
        self.assertTrue(self.partner_main.message_follower_ids)
        message = self.send_email_cc()
        self.assertTrue(self.partner_main_email in message.body_html)
        self.assertTrue(self.partner_follower_email in message.body_html)
        self.assertTrue(self.internal_user_1_email in message.body_html)
        self.assertTrue(self.internal_user_2_email in message.body_html)
        self.assertTrue("CC" in message.body_html)

    def test_show_cc_contacts_hide_all_internal(self):
        company = self.env.company
        self.assertTrue(company.show_internal_users_cc)
        company.write({"show_internal_users_cc": False})
        self.assertFalse(company.show_internal_users_cc)
        message = self.send_email_cc()
        self.assertTrue(self.partner_main_email in message.body_html)
        self.assertTrue(self.partner_follower_email in message.body_html)
        self.assertFalse(self.internal_user_1_email in message.body_html)
        self.assertFalse(self.internal_user_2_email in message.body_html)
        self.assertTrue("CC" in message.body_html)

    def test_show_cc_contacts_hide_single_internal(self):
        company = self.env.company
        self.assertTrue(company.show_internal_users_cc)
        self.assertTrue(self.internal_user_1.show_in_cc)
        self.internal_user_1.write({"show_in_cc": False})
        self.assertFalse(self.internal_user_1.show_in_cc)
        message = self.send_email_cc()
        self.assertTrue(self.partner_main_email in message.body_html)
        self.assertTrue(self.partner_follower_email in message.body_html)
        self.assertFalse(self.internal_user_1_email in message.body_html)
        self.assertTrue(self.internal_user_2_email in message.body_html)
        self.assertTrue("CC" in message.body_html)

    def test_show_cc_contacts_block_model(self):
        company = self.env.company
        self.assertFalse(company.cc_blocked_models)
        partner_model = self.env["ir.model"].search(
            [("model", "=", "res.partner")], limit=1
        )
        company.write({"cc_blocked_models": [partner_model.id]})
        self.assertTrue(company.cc_blocked_models)
        message = self.send_email_cc()
        self.assertFalse(self.partner_main_email in message.body_html)
        self.assertFalse(self.partner_follower_email in message.body_html)
        self.assertFalse(self.internal_user_1_email in message.body_html)
        self.assertFalse(self.internal_user_2_email in message.body_html)
        self.assertFalse("CC" in message.body_html)

    def test_show_cc_single(self):
        company = self.env.company
        company.write({"show_internal_users_cc": False})
        self.partner_main.message_unsubscribe(partner_ids=[self.partner_follower.id])
        message = self.send_email_cc()
        self.assertFalse("CC" in message.body_html)

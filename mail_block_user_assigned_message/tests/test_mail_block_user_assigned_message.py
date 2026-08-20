# Copyright 2026 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestMailBlockUserAssignedMessage(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_2 = cls.env.ref("base.user_demo")
        cls.notificable_record = cls.env["res.partner"].create({"name": "Test Partner"})
        # Set the registry as ready. If not, messages would not be sent
        # because this variable is checked before sending them
        cls.env.registry.ready = True

    def _turn_off_notificacions(self):
        self.user_2.partner_id.write(
            {
                "block_assigned_message": True,
                "block_assigned_message_model_ids": [
                    (4, self.env.ref("base.model_res_partner").id)
                ],
            }
        )

    def _get_notifications(self):
        return self.env["mail.message"].search(
            [("partner_ids", "in", self.user_2.partner_id.id)]
        )

    def test_message_blocked(self):
        notifications_before = len(self._get_notifications())
        self._turn_off_notificacions()
        self.notificable_record.write({"user_id": self.user_2.id})
        notifications_after = len(self._get_notifications())
        self.assertEqual(notifications_before, notifications_after)

    def test_message_not_blocked(self):
        notifications_before = len(self._get_notifications())
        self.notificable_record.write({"user_id": self.user_2.id})
        notifications_after = len(self._get_notifications())
        self.assertGreater(notifications_after, notifications_before)

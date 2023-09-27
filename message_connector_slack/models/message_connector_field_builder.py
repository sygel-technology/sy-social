# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class MessageConnectorFieldBuilder(models.Model):
    _inherit = "message.connector.field.builder"

    short = fields.Boolean(
        string="Short",
        help="Slack field to position the fields in two "
        "columns (Short = True) or in one (Short = False).",
        default=True,
    )
    separator_field_table = fields.Text(
        string="Separator",
        help="Separation between fields in a field table"
        "If left empty, a space will be placed between fields."
    )

    def _table_formatter(self, table):
        res = super()._table_formatter(table)
        if self.message_template_id.messaging_service == 'slack':
            value = ""
            separator = self.separator_field_table if\
                self.separator_field_table else " "
            for row in table:
                new_line = True
                for column in row:
                    value = "{}{}{}".format(
                        value,
                        separator if not new_line else "",
                        column
                    )
                    new_line = False
                value = "{}\n".format(value)
            res = value
        return res
                

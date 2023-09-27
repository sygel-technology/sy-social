# Copyright 2023 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Message Connector Slack",
    "summary": "Message Connector Slack",
    "version": "15.0.1.0.0",
    "category": "Custom",
    "website": "https://www.sygel.es",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": ["slackclient"]},
    "depends": [
        'message_connector_base'
    ],   
    "data": [
        "data/slack_data.xml",
        "views/message_connector_channel_views.xml",
        "views/message_connector_field_builder_views.xml",
        "views/message_connector_message_builder_views.xml",
        "views/message_connector_connection_views.xml",
        "views/res_config_settings_views.xml"
    ],
}

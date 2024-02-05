# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Mail Block User Assigned Message",
    "summary": "Block assignation notifications depending on model",
    "version": "16.0.1.0.0",
    "category": "Project",
    "website": "https://www.sygel.es",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "mail",
    ],    
    "data": [
        "views/res_users_views.xml",
    ],
}

import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-sygel-technology-sy-social",
    description="Meta package for sygel-technology-sy-social Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-disabled_mail_follower_invitation>=16.0dev,<16.1dev',
        'odoo-addon-mail_block_user_assigned_message>=16.0dev,<16.1dev',
        'odoo-addon-mail_hide_header_portal_button>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)

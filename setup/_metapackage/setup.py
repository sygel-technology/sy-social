import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-sygel-technology-sy-social",
    description="Meta package for sygel-technology-sy-social Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-disabled_mail_follower_invitation',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)

{
    'name': "Smart Sale Order Approvals",
    'version': '1.2',
    'summary': 'Smart Sale Order Approvals',
    'sequence': 100,
    'author': "JD DEVS",
    'depends': ['base', 'web_studio', 'sale' ],
    'assets': {
        'web.assets_backend': [
            "smart_sale_approval_studio/static/src/legacy/js/approval_component.js",
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/assets/screenshots/banner.png'],
}
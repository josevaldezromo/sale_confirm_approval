{
    'name': 'Sale Confirmation Approval',
    'version': '1.0.0',
    'category': 'Sales',
    'summary': 'Adds approval workflow for sale order confirmations',
    'description': """
Sale Confirmation Approval
===========================
This module adds a two-step confirmation process for sales orders:
- Users with sale_requires_approval=True need approval to confirm orders
- Users with sale_can_approve=True can approve pending orders
    """,
    'author': 'RaymundoValdez',
    'website': 'https://saturnonexus.com',
    'license': 'LGPL-3',
    'depends': [
        'sale_management',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

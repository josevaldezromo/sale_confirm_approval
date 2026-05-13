{
    'name': 'Autorización al Confirmar Cotización',
    'version': '18.0.1.0.1', # Incrementamos versión
    'summary': 'Intercepta el botón Confirmar y requiere autorización de Gerente',
    'category': 'Sales',
    'author': 'Raymundo Valdez',
    'depends': ['base', 'sale_management', 'mail'], # Agregamos base y mail
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
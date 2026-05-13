# -*- coding: utf-8 -*-
from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    sale_requires_approval = fields.Boolean(
        string='Requiere Aprobación en Ventas', 
        default=False,
        help="Si está marcado, sus cotizaciones deben ser aprobadas antes de confirmarse."
    )
    sale_can_approve = fields.Boolean(
        string='Puede Aprobar Ventas', 
        default=False,
        help="Permite a este usuario aprobar cotizaciones de otros."
    )
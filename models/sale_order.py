# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approval_state = fields.Selection([
        ('not_required', 'No requerida'),
        ('pending', 'Por Autorizar'),
        ('approved', 'Aprobada'),
        ('rejected', 'Rechazada'),
    ], string='Estado de Autorización', default='not_required', tracking=True, copy=False)
    
    approved_by = fields.Many2one('res.users', string='Autorizado por', readonly=True, copy=False)
    approval_date = fields.Datetime(string='Fecha de autorización', readonly=True, copy=False)

    def _requires_approval(self):
        self.ensure_one()
        return self.user_id.sale_requires_approval if self.user_id else False

    def action_request_approval(self):
        for order in self:
            if order.state not in ('draft', 'sent'):
                raise UserError(_("Solo puedes solicitar autorización en presupuestos."))
            
            order.sudo().write({'approval_state': 'pending'})
            order.message_post(body=_("Autorización solicitada al supervisor."))

            # --- NOTIFICACIÓN PUSH A LOS APROBADORES ---
            # Buscamos a los usuarios que tienen el permiso de aprobar
            approvers = self.env['res.users'].sudo().search([
                ('sale_can_approve', '=', True),
                ('active', '=', True)
            ])
            
            for approver in approvers:
                self.env['bus.bus']._sendone(approver.partner_id, 'simple_notification', {
                    'type': 'info',
                    'title': _('Solicitud de Aprobación'),
                    'message': _('La cotización %s requiere tu validación.') % order.name,
                    'sticky': True,
                })
        return True

    def action_approve_quotation(self):
        self.ensure_one()
        if not self.env.user.sale_can_approve and not self.env.user.has_group('sale_confirm_approval.group_sale_approver'):
            raise UserError(_("No tienes permisos de aprobador."))
        
        self.sudo().write({
            'approval_state': 'approved',
            'approved_by': self.env.uid,
            'approval_date': fields.Datetime.now()
        })
        self.message_post(body=_("Cotización aprobada."))

        # --- NOTIFICACIÓN PUSH AL VENDEDOR ---
        if self.user_id:
            self.env['bus.bus']._sendone(self.user_id.partner_id, 'simple_notification', {
                'type': 'success',
                'title': _('Cotización Aprobada'),
                'message': _('Tu cotización %s ha sido autorizada.') % self.name,
                'sticky': False,
            })
        return True

    def action_reject_quotation(self):
        self.ensure_one()
        if not self.env.user.sale_can_approve and not self.env.user.has_group('sale_confirm_approval.group_sale_approver'):
            raise UserError(_("No tienes permisos de aprobador."))
        
        self.sudo().write({'approval_state': 'rejected'})
        self.message_post(body=_("Cotización rechazada por el supervisor."))

        # --- NOTIFICACIÓN PUSH AL VENDEDOR ---
        if self.user_id:
            self.env['bus.bus']._sendone(self.user_id.partner_id, 'simple_notification', {
                'type': 'danger',
                'title': _('Cotización Rechazada'),
                'message': _('La cotización %s no fue autorizada.') % self.name,
                'sticky': True,
            })
        return True

    def action_confirm(self):
        for order in self:
            if order._requires_approval() and order.approval_state != 'approved':
                if order.approval_state == 'pending':
                    raise UserError(_("Esta cotización está pendiente de autorización."))
                else:
                    raise UserError(_("Debes solicitar autorización antes de confirmar esta venta."))
        
        return super(SaleOrder, self).action_confirm()

    def action_draft(self):
        res = super(SaleOrder, self).action_draft()
        self.sudo().write({
            'approval_state': 'not_required',
            'approved_by': False,
            'approval_date': False
        })
        return res
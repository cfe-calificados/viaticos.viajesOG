# -*- coding: utf-8 -*-

from five import grok

from viaticos.viajes.content.viaje import IViaje

from Products.CMFCore.utils import getToolByName

from datetime import datetime

from plone import api

import ast

class CanSendToAgency(grok.View):
    grok.context(IViaje)
    grok.name("can-send-to-agency")
    grok.require("zope2.View")

    def __call__(self):
        print("im a transition guard and i'm getting called!!")
        portal = api.portal.get()
        pm = getToolByName(self.context, 'portal_membership')
        auth_member = pm.getAuthenticatedMember()
        viaje = self.context
        status = api.content.get_state(obj=portal["viaticos"][viaje.id])
        obj_owner = viaje.getOwner()
        upward = pm.getMemberById(obj_owner.getUserId()).getProperty("downward")
        upward_dic = {}
        try:
            upward_dic = ast.literal_eval(upward)
        except SyntaxError:
            print("Missing hierarchy for "+obj_owner)

        #import pdb; pdb.set_trace()
        #Switch
        if status == "borrador":
            if auth_member.getUser().getUserName() == obj_owner.getUserName():
                print("Es owner")
                horas_diff = (self.context.fecha_salida-datetime.now()).total_seconds()/3600
                print(horas_diff)
                if 'anticipo' in viaje.req and horas_diff < 48 :                    
                    return False
                catalog = api.portal.get_tool('portal_catalog')
                brains = [x for x in catalog.queryCatalog({"portal_type": "comprobacion", "review_state": ["bosquejo","revision finanzas", "revision implant"], "Creator": auth_member.getUser().getId()}) if (datetime.now()-x.created.asdatetime().replace(tzinfo=None)).days > 5]
                return not brains
                    
            else:
                print("No es owner")
                return False
        if (auth_member.has_role('Manager') or auth_member.has_role('Finanzas')) and status != "esperando agencia":
            print(status,"Es admin, puede hacer transicion")
            return True
        if status == "revision aprobador":
            if upward_dic.has_key(auth_member.getUser().getUserName()):
                if viaje.grupo and auth_member.getUser().getUserName() in viaje.grupo:
                    print("Es jefe del owner, y puede autorizar su propio viaje.")
                    return True
                print("Es jefe del owner, puede hacer transicion")
                return True
            print("Es jefe pero no del owner, no puede hacer transicion")
            return False
        if status == "esperando agencia" and (auth_member.has_role('Manager') or auth_member.has_role('Implant')):
            print("Es administrador o implant y puede enviar anticipo")
            return ((viaje.aerolinea != None and viaje.tarifa != None and viaje.hora_regreso != None and viaje.hora_salida != None) or 'boleto_avion' not in viaje.req) and ((viaje.hotel_nombre != None and viaje.hotel_domicilio != None) or 'hospedaje' not in viaje.req) and ('transporte_terrestre' not in viaje.req or (viaje.trans_empresa != None and viaje.trans_desc != None and viaje.trans_reserv != None and viaje.trans_pago != None)) and ('otro' not in viaje.req or (viaje.otro_empresa != None and viaje.otro_desc != None and viaje.otro_reserv != None and viaje.otro_pago != None)) and (viaje.anti_desc != None and viaje.anti_monto != None)
        print(status)
        return False #if not the admin, not possible

        

    def render(self):
        return "can-send-to-agency"



class CanSendToAdmin(grok.View):
    grok.context(IViaje)
    grok.name("can-send-to-admin")
    grok.require("zope2.View")

    def __call__(self):
        print("im a transition guard and i'm getting called!!")
        portal = api.portal.get()
        pm = getToolByName(self.context, 'portal_membership')
        auth_member = pm.getAuthenticatedMember()
        viaje = self.context
        status = api.content.get_state(obj=portal["viaticos"][viaje.id])
        obj_owner = viaje.getOwner()

        if status == "borrador":
            if auth_member.getUser().getUserName() == obj_owner.getUserName():
                print("Es owner")
                horas_diff = (self.context.fecha_salida-datetime.now()).total_seconds()/3600
                print(horas_diff)
                if 'anticipo' in viaje.req and horas_diff < -24:                    
                    catalog = api.portal.get_tool('portal_catalog')
                    brains = [x for x in catalog.queryCatalog({"portal_type": "comprobacion", "review_state": ["bosquejo","revision finanzas", "revision implant"], "Creator": auth_member.getUser().getId()}) if (datetime.now()-x.created.asdatetime().replace(tzinfo=None)).days > 5]
                    return not brains
            
        if auth_member.has_role('Manager'):
            print(status,"Es admin, puede hacer transicion")
            return True

        return False
        

    def render(self):
        return "can-send-to-admin"

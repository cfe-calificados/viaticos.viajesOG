# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone.dexterity.browser.view import DefaultView
from plone import api
from form import TicketForm
from Products.CMFCore.utils import getToolByName

class VistaViaje(DefaultView):
    """ Vista por defecto para viajes/solicitud de gastos """

    def values_setted(self):
        objeto = self.context
        return objeto.aerolinea != None and objeto.tarifa != None and objeto.hora_regreso != None and objeto.hora_salida != None and objeto.hotel_nombre != None and objeto.hotel_domicilio != None 
        
    def is_transact_state(self):
        print("checking obj state")
        #import pdb; pdb.set_trace()
        portal = api.portal.get()
        status = api.content.get_state(obj=portal["viaticos"][self.context.id])
        return True if status == "esperando" else False
        
    def render_ticket_form(self):
        #import pdb; pdb.set_trace()
        print("trying...")
        form = TicketForm(self.context, self.request)
        form.update()
        return form

    def valid_registration(self):
        return True


class VistaComprobacion(DefaultView):
    """ Vista por defecto para comprobacion de gastos """
    def get_viaje(self):
        obj_comp = self.context
        catalog = api.portal.get_tool('portal_catalog')
        if obj_comp.relacion.isBroken():
            print("Relación a viaje rota")
            return None
        brains = catalog(path={'query': obj_comp.relacion.to_path, 'depth': 0})
        return brains[0].getObject()

    def get_file_idx(self, concepto):
        return self.context.grupo_comprobacion.index(concepto)
        
        
        
        

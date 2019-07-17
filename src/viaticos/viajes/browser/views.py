# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone.dexterity.browser.view import DefaultView
from plone import api
from form import TicketForm
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.resources import add_resource_on_request
#Auth purposes
from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from Products.CMFCore.permissions import AddPortalContent

class VistaViaje(DefaultView):
    """ Vista por defecto para viajes/solicitud de gastos """

    def get_info_state(self):
        portal = api.portal.get()
        status = api.content.get_state(obj=portal["viaticos"][self.context.id])
        out = ""
        if status != 'final':
            out = "Este elemento se encuentra en el estado '"+status+"', por lo que aún está en proceso de registro. En la barra de herramientas encontrará las posibles transiciones de este objeto."
        return out
    
    def requirements(self):
        return "boleto_avion" in self.context.req or "hospedaje" in self.context.req

    def values_setted(self):
        objeto = self.context        
        avion_bool = objeto.aerolinea != None and objeto.tarifa != None and objeto.hora_regreso != None and objeto.hora_salida != None  
        hotel_bool = objeto.hotel_nombre != None and objeto.hotel_domicilio != None
        if "boleto_avion" in objeto.req and 'hospedaje' in objeto.req:
            return avion_bool and hotel_bool
        if "boleto_avion" in objeto.req and 'hospedaje' not in objeto.req:
            return avion_bool
        if "boleto_avion" not in objeto.req and 'hospedaje' in objeto.req:
            return hotel_bool
        return False
                                     
        
        
    def is_transact_state(self):
        print("checking obj state")
        #import pdb; pdb.set_trace()
        portal = api.portal.get()
        status = api.content.get_state(obj=portal["viaticos"][self.context.id])
        is_owner = self.context.portal_membership.getAuthenticatedMember().getUser().getUserName() == self.context.getOwner().getUserName()
        needs_ticket = 'boleto_avion' in self.context.req or 'hospedaje' in self.context.req
        return True if status == "esperando" and is_owner else False
        
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
        
        
        
        
class VistaViaticos(BrowserView):
    """ Una vista para listar solicitudes y comprobaciones de gastos
    """

    def __call__(self):
        sm = getSecurityManager()
        if not sm.checkPermission(AddPortalContent, self):
            raise Unauthorized("Contenido inaccesible para usuarios no registrados. Por favor inicie sesión.")
        # utility function to add resource to rendered page
        print("loading CSS")        
        add_resource_on_request(self.request, 'tabs_statics')
        return super(VistaViaticos, self).__call__()

    
    def is_boss(self):
        current_user = self.context.portal_membership.getAuthenticatedMember().getUser()
        return current_user.has_role("Manager") or current_user.has_role("Reader")

    def viajes(self):        
        results = [[],[]]
        brains = api.content.find(context=self.context, portal_type='viaje')

        for brain in brains:            
            viaje = brain.getObject()
            portal = brain.portal_url.getPortalObject()
            is_owner = self.context.portal_membership.getAuthenticatedMember().getUser().getUserName() == viaje.getOwner().getUserName()
            idx = 0 if is_owner else 1
            results[idx].append({
                'title': brain.Title,#with url brain.getURL()
                'creator': brain.Creator,
                'creator_url': portal.absolute_url()+'/author/'+brain.Creator,
                'state': api.content.get_state(obj=portal["viaticos"][viaje.id]),
                'modif_date':viaje.modified().strftime("%Y-%m-%d %H:%M:%S"),#  ,               
                'uuid': brain.UID,
                'url': brain.getURL(),
                'motivo': viaje.motivo,#,
            })
            
        return results

    def comprobaciones(self):
        
        results = [[],[]]
        brains = api.content.find(context=self.context, portal_type='comprobacion')
        #import pdb; pdb.set_trace(

        for brain in brains:            
            comprobacion = brain.getObject()
            portal = brain.portal_url.getPortalObject()
            is_owner = self.context.portal_membership.getAuthenticatedMember().getUser().getUserName() == comprobacion.getOwner().getUserName()
            idx = 0 if is_owner else 1

            viaje = None
            catalog = api.portal.get_tool('portal_catalog')
            if not comprobacion.relacion.isBroken():            
                brains = catalog(path={'query': comprobacion.relacion.to_path, 'depth': 0})
                viaje = brains[0].getObject()
                
            results[idx].append({
                'title': brain.Title,#with url brain.getURL()
                'creator': brain.Creator,
                'creator_url': portal.absolute_url()+'/'+brain.Creator,
                'state': api.content.get_state(obj=portal["viaticos"][comprobacion.id]),
                'modif_date':comprobacion.modified().strftime("%Y-%m-%d %H:%M:%S"),#  ,               
                'uuid': brain.UID,
                'url': brain.getURL(),
                'viaje': viaje.Title,
                'viaje_url': viaje.absolute_url()
            })
        return results

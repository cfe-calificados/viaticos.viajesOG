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
#sorting
from operator import itemgetter as get_item
import ast        

class VistaViaje(DefaultView):
    """ Vista por defecto para viajes/solicitud de gastos """
    def check_group(self, username, grupo):
        if username in grupo:
            return True
        membership = getToolByName(self.context, 'portal_membership')
        downward = membership.getMemberById(username).getProperty("downward")
        downward_dic = {}
        try:
            downward_dic = ast.literal_eval(downward)
        except SyntaxError:
            print("Missing hierarchy for "+username)

        for employee in grupo:
            tmp = {}
            downward = membership.getMemberById(employee).getProperty("downward")
            try:
                tmp = ast.literal_eval(downward)
            except SyntaxError:
                print("Missing hierarchy for "+employee)            
            downward_dic.update(tmp)
            
        if downward_dic == None: return False
        if downward_dic.has_key(username):                    
            return True
        return False
    
    def is_boss(self):
        current_user = self.context.portal_membership.getAuthenticatedMember().getUser()
        return current_user.has_role("Manager") or current_user.has_role("Reader")

    def __call__(self):
        auth_member = self.context.portal_membership.getAuthenticatedMember()
        if auth_member.has_role('Manager'):
            return super(VistaViaje, self).__call__()
        current_user = auth_member.getUser().getUserName()
        upward_dic = {}
        obj_owner = self.context.getOwner()
        try:
            membership = getToolByName(self.context, 'portal_membership')
            upward = membership.getMemberById(obj_owner.getUserId()).getProperty("downward")
            upward_dic = ast.literal_eval(upward)
        except Exception:
            print("Missing hierarchy")
        if self.context.grupo:#this is more time of processing :C
            if self.check_group(current_user, self.context.grupo):
                return super(VistaViaje, self).__call__()
        if not upward_dic.has_key(current_user) and not current_user == obj_owner.getUserId():        
            raise Unauthorized("Contenido inaccesible para miembros no supervisores o que no pertenecen a este grupo.")        
        return super(VistaViaje, self).__call__()


    def get_info_state(self):
        portal = api.portal.get()
        status = api.content.get_state(obj=portal["viaticos"][self.context.id])
        out = ""
        if status != 'final':
            out = "Este elemento se encuentra en el estado '"+status+"', por lo que aún está en proceso de registro. En la barra de herramientas encontrará las posibles transiciones de este objeto."
        return out
    
    def requirements(self):
        current_user = self.context.portal_membership.getAuthenticatedMember()
        return current_user.has_role('Manager')

    def values_setted(self):
        viaje = self.context        
        return ((viaje.aerolinea != None and viaje.tarifa != None and viaje.hora_regreso != None and viaje.hora_salida != None) or 'boleto_avion' not in viaje.req) and ((viaje.hotel_nombre != None and viaje.hotel_domicilio != None) or 'hospedaje' not in viaje.req) and ('transporte_terrestre' not in viaje.req or (viaje.trans_empresa != None and viaje.trans_desc != None and viaje.trans_reserv != None and viaje.trans_pago != None)) and ('otro' not in viaje.req or (viaje.otro_empresa != None and viaje.otro_desc != None and viaje.otro_reserv != None and viaje.otro_pago != None)) and (viaje.anti_desc != None and viaje.anti_monto != None)
                                     

    def is_pending_state(self):
        portal = api.portal.get()
        status = api.content.get_state(obj=portal["viaticos"][self.context.id])
        return True if status == "revision_aprobador" and self.is_boss() else False
        
        
    def is_transact_state(self):
        print("checking obj state")
        #import pdb; pdb.set_trace()
        portal = api.portal.get()
        status = api.content.get_state(obj=portal["viaticos"][self.context.id])
        #is_owner = self.context.portal_membership.getAuthenticatedMember().getUser().getUserName() == self.context.getOwner().getUserName()
        #needs_ticket = 'boleto_avion' in self.context.req or 'hospedaje' in self.context.req
        return True if status == "esperando_agencia" and self.is_boss() else False#is_owner else False
        
    def render_ticket_form(self):
        #import pdb; pdb.set_trace()
        print("trying...")
        form = TicketForm(self.context, self.request)
        form.update()
        #form.updateFields()
        return form

    def valid_registration(self):
        return self.context.getOwner().getUserName() != self.context.portal_membership.getAuthenticatedMember().getUser().getUserName()


class VistaComprobacion(DefaultView):
    """ Vista por defecto para comprobacion de gastos """

    convert = {1:"Taxis",2:"Boletos de avión",3:"Boletos de avión",4:"Gasolina",5:"Autopista",6:"Estacionamiento",7:"Hospedaje",8:"Alimentos",9:"Gastos especiales"}    

    def __call__(self):
        auth_member = self.context.portal_membership.getAuthenticatedMember()        
        if auth_member.has_role('Manager'):
            return super(VistaComprobacion, self).__call__()
        current_user = auth_member.getUser().getUserName()
        upward_dic = None
        obj_owner = self.context.getOwner()
        try:
            membership = getToolByName(self.context, 'portal_membership')
            upward = membership.getMemberById(obj_owner.getUserId()).getProperty("downward")
            upward_dic = ast.literal_eval(upward)
        except SyntaxError:
            print("Missing hierarchy for "+self.context.Title)
        if upward_dic == None or (not upward_dic.has_key(current_user) and not current_user == obj_owner.getUserId()):        
            raise Unauthorized("Contenido inaccesible para miembros no supervisores o que no pertenecen a este grupo.")        
        return super(VistaComprobacion, self).__call__()
        
    
    def get_info_state(self):
        portal = api.portal.get()
        status = api.content.get_state(obj=portal["viaticos"][self.context.id])
        out = ""
        if status != 'aprobado':
            out = "Este elemento se encuentra en el estado '"+status+"', por lo que aún está en proceso de registro. En la barra de herramientas encontrará las posibles transiciones de este objeto."
        return out

    
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

    def calc_saldo(self):
        tupla_totales = []
        conceptos = self.context.grupo_comprobacion
        total = self.context.total_comprobar*-1
        tupla_totales.append(total)
        tupla_totales.append(0.0)
        for concepto in conceptos:
            if concepto['anticipo'] == "reembolso":
                tupla_totales[1] += concepto['comprobado']
                continue
            if concepto['importe'] <= concepto['comprobado']:
                tupla_totales[0] += concepto['importe']
            else:
                tupla_totales[0] += concepto['comprobado']
        
        return tupla_totales+['{:,}'.format(tupla_totales[0]+tupla_totales[1])]

    def get_clave(self,concepto):
        return self.convert[concepto]

    def confirm_reset(self):
        return "confirmar('¿Está seguro de reiniciar la información de comprobaciones? Perderá toda la información que ha añadido hasta ahora.')"

    def get_status(self):
        portal = api.portal.get()
        status = api.content.get_state(obj=portal["viaticos"][self.context.id])
        return status
        
        
        
        
class VistaViaticos(BrowserView):
    """ Una vista para listar solicitudes y comprobaciones de gastos
    """

    order = {'borrador': 1, 'revision_aprobador': 2, 'esperando_agencia':3, 'anticipo_pendiente':4, 'final':5}
    get_states = {1:'borrador', 2:'revision_aprobador', 3:'esperando_agencia', 4:'anticipo_pendiente', 5:'final'}
    orden = {'bosquejo': 1,'revision': 2, 'aprobado': 3}
    get_comp = {1:'bosquejo', 2:'revision', 3:'aprobado'} 

    def order_by_state_date(self,owned_supervised):
        owned = sorted(sorted(owned_supervised[0], key=lambda k: k['modif_date'], reverse=True), key=lambda k: k['state'])
        supervised = sorted(sorted(owned_supervised[1], key=lambda k: k['modif_date'], reverse=True), key=lambda k: k['state'])
        return [owned, supervised]

    def __call__(self):
        sm = getSecurityManager()
        if not sm.checkPermission(AddPortalContent, self):
            raise Unauthorized("Contenido inaccesible para usuarios no registrados. Por favor inicie sesión.")
        # utility function to add resource to rendered page
        print("loading CSS")        
        add_resource_on_request(self.request, 'tabs_statics')
        return super(VistaViaticos, self).__call__()

    def get_upward_url(self):
        current_user = self.context.portal_membership.getAuthenticatedMember()
        return "/".join([self.context.absolute_url(),"@@upward-form"]) if current_user.has_role('Manager') else ""
    
    def is_boss(self):
        current_user = self.context.portal_membership.getAuthenticatedMember().getUser()
        return current_user.has_role("Manager") or current_user.has_role("Reader")

    def check_group(self, username, grupo):
        if username in grupo:
            return True
        membership = getToolByName(self.context, 'portal_membership')
        downward = membership.getMemberById(username).getProperty("downward")
        downward_dic = {}
        try:
            downward_dic = ast.literal_eval(downward)
        except SyntaxError:
            print("Missing hierarchy for "+username)

        for employee in grupo:
            tmp = {}
            downward = membership.getMemberById(employee).getProperty("downward")
            try:
                tmp = ast.literal_eval(downward)
            except SyntaxError:
                print("Missing hierarchy for "+employee)            
            downward_dic.update(tmp)
            
        if downward_dic == None: return False
        if downward_dic.has_key(username):                    
            return True
        return False

    def viajes(self):        
        results = [[],[]]
        #brains = api.content.find(context=self.context, portal_type='viaje')#aqui haremos la query mediante el owner o creador.
        auth_member = self.context.portal_membership.getAuthenticatedMember()
        owner_username = auth_member.getUser().getUserName()
        portal_ctl = self.context.portal_catalog
        membership = getToolByName(self.context, 'portal_membership')
        brains = []
        for x in portal_ctl({'portal_type':'viaje'}):
            obj_tmp = x.getObject()
            obj_owner = obj_tmp.getOwner()
            if auth_member.has_role('Manager'):
                brains.append(x)
                continue
            downward = membership.getMemberById(obj_owner.getUserId()).getProperty("downward")
            downward_dic = None
            try:
                downward_dic = ast.literal_eval(downward)
            except SyntaxError:
                print("Missing hierarchy for "+x.Creator)
            if downward_dic == None: continue
            if downward_dic.has_key(owner_username) or owner_username == obj_owner.getUserId():
                brains.append(x)
                continue
            if obj_tmp.grupo:#this is more time of processing :C we try to skip it whenever possible
                if self.check_group(owner_username, obj_tmp.grupo):
                    brains.append(x)
        
        for brain in brains:            
            viaje = brain.getObject()
            portal = brain.portal_url.getPortalObject()
            is_owner = owner_username == viaje.getOwner().getUserName() or owner_username in viaje.grupo
            idx = 0 if is_owner else 1
            results[idx].append({
                'title': brain.Title,#with url brain.getURL()
                'creator': viaje.getOwner().getId(),
                'creator_url': portal.absolute_url()+'/author/'+viaje.getOwner().getId(),
                'state': self.order[api.content.get_state(obj=portal["viaticos"][viaje.id])],
                'modif_date':viaje.modified().strftime("%Y-%m-%d %H:%M:%S"),
                'uuid': brain.UID,
                'url': brain.getURL(),
                'motivo': viaje.motivo,#,
            })
            
        return self.order_by_state_date(results)

    def comprobaciones(self):
        
        results = [[],[]]
        #brains = api.content.find(context=self.context, portal_type='comprobacion')
        #import pdb; pdb.set_trace(
        auth_member = self.context.portal_membership.getAuthenticatedMember()
        owner_username = auth_member.getUser().getUserName()
        portal_ctl = self.context.portal_catalog
        membership = getToolByName(self.context, 'portal_membership')
        brains = []
        #import pdb; pdb.set_trace()
        for x in portal_ctl({'portal_type':'comprobacion'}):
            obj_owner = x.getObject().getOwner()
            if auth_member.has_role("Manager"):
                brains.append(x)
                continue
            downward = membership.getMemberById(obj_owner.getUserId()).getProperty("downward")
            downward_dic = None
            try:
                downward_dic = ast.literal_eval(downward)
            except SyntaxError:
                print("Missing hierarchy for "+x.Creator)
            if downward_dic == None: continue
            #import pdb; pdb.set_trace()
            if downward_dic.has_key(owner_username) or owner_username == obj_owner.getUserId():
                brains.append(x)                            
 
        for brain in brains:            
            comprobacion = brain.getObject()
            portal = brain.portal_url.getPortalObject()
            is_owner = owner_username == comprobacion.getOwner().getUserName()
            idx = 0 if is_owner else 1

            viaje = None
            catalog = api.portal.get_tool('portal_catalog')
            if not comprobacion.relacion.isBroken():            
                brains = catalog(path={'query': comprobacion.relacion.to_path, 'depth': 0})
                viaje = brains[0].getObject()
                
            results[idx].append({
                'title': brain.Title,#with url brain.getURL()
                'creator': comprobacion.getOwner().getId(),
                'creator_url': portal.absolute_url()+'/author/'+comprobacion.getOwner().getId(),
                'state': self.orden[api.content.get_state(obj=portal["viaticos"][comprobacion.id])],
                'modif_date':comprobacion.modified().strftime("%Y-%m-%d %H:%M:%S"),#  ,               
                'uuid': brain.UID,
                'url': brain.getURL(),
                'viaje': viaje.Title,
                'viaje_url': viaje.absolute_url()
            })
        return self.order_by_state_date(results)

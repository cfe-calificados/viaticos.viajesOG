# -*- coding: utf-8 -*-
from plone.directives import form
from z3c.form import field
from z3c.form.form import extends
from zope import interface
from zope import component
from zope import schema
from viaticos.viajes import _
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from z3c.form import button
from plone.app.vocabularies.catalog import CatalogSource, CatalogVocabulary
from plone.dexterity.browser.view import DefaultView
from Products.Five.browser import BrowserView
# For membership purposes
from Products.CMFCore.utils import getToolByName
from zope.schema.interfaces import IContextAwareDefaultFactory
from ast import literal_eval
import json
## For group purposes
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from zope.interface import provider
import ast
from zope.schema.interfaces import IContextSourceBinder

Coordinaciones = SimpleVocabulary(
    [SimpleTerm(value=u'administracion', title=_(u'Administración')),
     SimpleTerm(value=u'servicio_cliente', title=_(u'Atención y servicio al cliente')),
     SimpleTerm(value=u'comercial', title=_(u'Comercial')),
     SimpleTerm(value=u'finanzas', title=_(u'Finanzas')), 
     SimpleTerm(value=u'gestion_energia', title=_(u'Gestión de energía')),
     SimpleTerm(value=u'juridico', title=_(u'Jurídico')),
    ]
)

class IUpwardForm(form.Schema):
    miembro = schema.Choice(
        title = _(u'Miembro'),
        vocabulary=u"plone.app.vocabularies.Users",
        required = True,
        default=None
    )

    coordinacion = schema.Choice(
        title=_(u'Coordinación'),
        vocabulary=Coordinaciones,
        required=True        
    )
    
    up_members = schema.List(
        title=_(u'Superiores'),
        description=_(u'Agregar lista de miembros con permiso de lectura (Disponibles | Actuales)'),        
        value_type=schema.Choice(
            title=_(u"Miembro"),
            vocabulary = u"plone.app.vocabularies.Users",
            required = True,
        ),
        #default = [],
        required=True
    )

class UpwardForm(form.SchemaForm):
    schema = IUpwardForm
    label = u"Organización de usuarios"
    description = u"Establece quiénes pueden ver el contenido del miembro seleccionado."
    ignoreContext = True

    members_selected = {}
    members_avail = []
    employee_area = ""
    def update_member(self, data):
        #import pdb; pdb.set_trace()
        if not (data['miembro'] and data['coordinacion']):
            self.status = u"No se puede continuar con una selección vacía"
            return
        try:
            data['up_members'].remove(data['miembro'])
        except ValueError:
            pass
        upward = "{'"+"': 1, '".join(data['up_members'])+"': 1}"
        #",".join(data['up_members'])
        membership = getToolByName(self.context, 'portal_membership')
        member = membership.getMemberById(data['miembro'])
        print(upward)
        if data['up_members']:
            member.setMemberProperties(mapping={"downward": upward, "coordinacion":data['coordinacion']})
        else:
            member.setMemberProperties(mapping={"coordinacion":data['coordinacion']})
        self.status = "Miembros superiores asignados exitosamente."
        return 

    @button.buttonAndHandler(u'Aceptar')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.update_member(data)
        #import pdb; pdb.set_trace()
        return
    
    @button.buttonAndHandler(u"Cancelar")
    def handleCancel(self, action):
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(u"Rellenar")
    def handleFill(self, action):
        data, errors = self.extractData()
        membership = getToolByName(self.context, 'portal_membership')
        miembro = membership.getMemberById(data['miembro'])
        downward = miembro.getProperty("downward")
        
        if downward:
            self.members_selected = literal_eval(downward)        
        self.members_avail = []
        for member in membership.listMembers():        
            if member.has_role("Reader") and not self.members_selected.has_key(member.getProperty("id")) and member != miembro:
                self.members_avail.append({"option":member.getProperty("fullname").decode('utf-8').encode('latin_1'), "value":str(member)})
        new_selected = []
        for boss in self.members_selected:
            new_selected.append({"option": membership.getMemberById(boss).getProperty("fullname").decode('utf-8').encode('latin_1'), "value":boss})
        self.members_selected = new_selected

        # Set Coordinacion
        coordinacion = miembro.getProperty("coordinacion")
        if coordinacion:
            self.employee_area = coordinacion
        return


    def updateActions(self):
        super(UpwardForm, self).updateActions()
        self.actions["aceptar"].addClass("context")
        self.actions["cancelar"].addClass("standalone")
    

class VistaJerarquia(BrowserView):

    def get_members(self, user_id=None):
        #import pdb; pdb.set_trace()
        print([self.form.members_avail, self.form.members_selected, self.form.employee_area])
        return [self.form.members_avail, self.form.members_selected, self.form.employee_area]
        
    def render_hierarchy_form(self):
        #import pdb; pdb.set_trace()
        print("trying...")
        self.form = UpwardForm(self.context, self.request)
        self.form.update()
        return self.form



def make_terms(items):
    """ Create zope.schema terms for vocab from tuples """
    terms = [ SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items ]
    return terms

def allowed_group(context):
    if context == None or not context.grupo: return ()
    #import pdb; pdb.set_trace()
    #return context.grupo
    out = []
    owner = context.getOwner().getUserName()
    auth_user = context.portal_membership.getAuthenticatedMember()
    if owner in context.grupo:
        context.grupo.remove(owner)
    if auth_user.has_role("Manager"):        
        return context.grupo

    auth_member = auth_user.getUser().getUserName()
    for person in context.grupo:
        if person == owner:
            continue
        upward_dic = {}
        membership = getToolByName(context, 'portal_membership')
        downward = membership.getMemberById(person).getProperty("downward")
        try:
            upward_dic = ast.literal_eval(downward)
        except SyntaxError:
            print("Missing hierarchy for "+person)
        if upward_dic.has_key(auth_member):
            out.append(person)
    print(out)
    return out

@provider(IContextAwareDefaultFactory)
def get_allowed_grupo(context):
    if context == None or context.grupo == None: return None
    return tuple(allowed_group(context))

@provider(IContextSourceBinder)
def get_allowed_voca(context):
    #from plone.app.vocabularies import Users
    #return Users
    if context == None or context.grupo == None: return None
    return SimpleVocabulary(make_terms([[x,x] for x in allowed_group(context)]))


class IVistaViajeros(form.Schema):
    #form.widget(grupo=AjaxSelectFieldWidget)
    grupo = schema.Tuple(
        title=_(u'Grupo'),
        description=u"Solicitud de gastos de varios empleados. Guardados | Por eliminar",    
        value_type=schema.Choice(
            source=get_allowed_voca,
        ),
        defaultFactory=get_allowed_grupo,
        required=False,         
        missing_value=()
    )

class VistaViajeros(form.SchemaForm):
    schema = IVistaViajeros
    label = u"Exclusión de miembros en Solicitud de gastos"
    description = u"Permite a los supervisores eliminar usuarios de un grupo de solicitud de gastos"
    ignoreContext = True

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

    def __call__(self):
        print("heehheee")
        auth_member = self.context.portal_membership.getAuthenticatedMember()
        if auth_member.has_role('Manager'):
            return super(VistaViajeros, self).__call__()
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
                return super(VistaViajeros, self).__call__()
        if not upward_dic.has_key(current_user) and not current_user == obj_owner.getUserId():        
            raise Unauthorized("Contenido inaccesible para miembros no supervisores o que no pertenecen a este grupo.")        
        return super(VistaViajeros, self).__call__()

    @button.buttonAndHandler(u'Aceptar')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        l_data = list(data['grupo'])
        ctx_list = list(self.context.grupo)
        for employee in l_data:
            ctx_list.remove(employee)
        self.context.grupo = tuple(ctx_list)
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(u'Cancelar')
    def handleCancel(self, action):
        self.request.response.redirect(self.context.absolute_url())

    def updateActions(self):
        super(VistaViajeros, self).updateActions()
        self.actions["aceptar"].addClass("context")
        self.actions["cancelar"].addClass("standalone")

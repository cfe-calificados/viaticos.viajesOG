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

class IUpwardForm(form.Schema):
    miembro = schema.Choice(
        title = _(u'Miembro'),
        vocabulary=u"plone.app.vocabularies.Users",
        required = True,
        default=None
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
    label = u"Jerarquía de usuarios"
    description = u"Establece quiénes pueden ver el contenido del miembro seleccionado."
    ignoreContext = True

    members_selected = {}
    members_avail = []
    def update_member(self, data):
        #import pdb; pdb.set_trace()
        if not (data['up_members'] and data['miembro']) :
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
        member.setMemberProperties(mapping={"downward": upward})
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
        import pdb; pdb.set_trace()
        return

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
            #import pdb; pdb.set_trace()
            if not self.members_selected.has_key(member.getProperty("id")) and member != miembro:
                self.members_avail.append({"option":member.getProperty("fullname").decode('utf-8').encode('latin_1'), "value":str(member)})
        new_selected = []
        for boss in self.members_selected:
            new_selected.append({"option": membership.getMemberById(boss).getProperty("fullname").decode('utf-8').encode('latin_1'), "value":boss})
        self.members_selected = new_selected
        return


    def updateActions(self):
        super(UpwardForm, self).updateActions()
        self.actions["aceptar"].addClass("context")
        self.actions["cancelar"].addClass("standalone")
    

class VistaJerarquia(BrowserView):

    def get_members(self, user_id=None):
        return [self.form.members_avail, self.form.members_selected]
        
    def render_hierarchy_form(self):
        #import pdb; pdb.set_trace()
        print("trying...")
        self.form = UpwardForm(self.context, self.request)
        self.form.update()
        return self.form

# -*- coding: utf-8 -*-
from plone.namedfile.field import NamedFile
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from viaticos.viajes import _
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
#for relationship purposes
from plone import api
from zope.schema.interfaces import IContextSourceBinder
from zope.interface import directlyProvides
from plone.app.vocabularies.catalog import CatalogSource, CatalogVocabulary
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.interface import provider
#for multiple files upload
#from plone.formwidget.multifile import MultiFileFieldWidget
from plone.formwidget.namedfile import NamedFileFieldWidget
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from zope import interface
from plone.app.z3cform.widget import DateFieldWidget
from plone.directives import form
from datetime import datetime
from plone.formwidget.namedfile.widget import NamedFileWidget
from zope.interface import implementer
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.browser import edit, add
from z3c.form import button, field
from z3c.relationfield import RelationValue, TemporaryRelationValue
from Products.CMFCore.utils import getToolByName
## for validation purposes
from zope.interface import Invalid
from zope.interface import invariant
#for omissions
from z3c.form.interfaces import IEditForm
from Products.CMFPlone.resources import add_resource_on_request
## vcb
from plone.app.z3cform.widget import AjaxSelectFieldWidget

claves_vcb = SimpleVocabulary(
    [SimpleTerm(value=1, title=_(u'Taxis')),
     SimpleTerm(value=2, title=_(u'Boletos de avión')),
     SimpleTerm(value=3, title=_(u'Boletos de autobús')),
     SimpleTerm(value=4, title=_(u'Gasolina')), 
     SimpleTerm(value=5, title=_(u'Autopista')),
     SimpleTerm(value=6, title=_(u'Estacionamiento')),
     SimpleTerm(value=7, title=_(u'Hospedaje')),
     SimpleTerm(value=8, title=_(u'Alimentos')),
     SimpleTerm(value=9, title=_(u'Gastos especiales')),
    ]
)

print("IComprobacion loaded")

#@provider(IContextAwareDefaultFactory)
def viaje_associated(context):
    #import pdb; pdb.set_trace()
    portal_catalog = api.portal.get_tool('portal_catalog')
    terms = []
    owner_trips= portal_catalog.searchResults(**{'portal_type':'viaje', 'review_state': 'final'})#api.user.get_current().getUser()})
    for x in owner_trips:
        print(x.getObject().title)
    for viaje in owner_trips:
        terms.append(SimpleVocabulary.createTerm(viaje, viaje.getObject().title, viaje.getObject().title))
    return SimpleVocabulary(terms)

directlyProvides(viaje_associated, IContextSourceBinder)

class ITable(interface.Interface):
    '''temporalmente lo quitamos para hacer la vista que no vulnere la seguridad por el widget '''
    directives.widget(
        'fecha',
        DateFieldWidget,         
        pattern_options={
            'today': False,
        }
    )    


    fecha = schema.Date(title=u"Fecha", required=True)
    clave = schema.Choice(title = _(u'Clave de gasto'), vocabulary=claves_vcb, required=True, default=None)
    concepto = schema.TextLine(title=u"Concepto",required=True)
    descripcion = schema.Text(title=u"Descripción",required=True)
    #directives.omitted(IEditForm, 'importe')
    #directives.write_permission(importe='cmf.ManagePortal')
    importe = schema.Float(title=u"Importe",required=True, default=0.0)    
    comprobado = schema.Float(title=u"Monto comprobado", default=0.0, required=True)

    #directives.omitted(IEditForm, 'anticipo')
    #directives.write_permission(anticipo='cmf.ManagePortal')
    anticipo = schema.Choice(title=_(u"Tipo"), vocabulary=SimpleVocabulary([SimpleTerm(value=u'anticipo', title=_(u'Por anticipo')), SimpleTerm(value=u'reembolso', title=_(u'Por reembolso'))]), default=u'reembolso', required=True)
    archivo = NamedFile(
        title=_(u'Archivo'),
        description=u"Usar comprimido para múltiples archivos.",
        required = True
    )

    directives.widget(
        'archivo',
        NamedFileFieldWidget
    )

    directives.widget(
        'anticipo',
        RadioFieldWidget
    )
    

class IComprobacion(model.Schema):
    """ Esquema dexterity para el tipo Comprobacion
    """

    directives.read_permission(relacion='zope2.View')
    directives.write_permission(relacion='cmf.ModifyPortalContent')
    directives.omitted(IEditForm, 'relacion')    
    relacion = RelationChoice(
        title=_(u'Solicitud'),
        source=CatalogSource(portal_type=['viaje'], review_state=['final']),#viaje_associatede,#
        required=True,
    )

    directives.read_permission(title='zope2.View')
    directives.write_permission(title='cmf.ModifyPortalContent')
    directives.omitted(IEditForm, 'title')
    #directives.omitted(IEditForm, 'title')    
    title = schema.TextLine(
        title=_(u'Título'),
    )

    directives.write_permission(total_comprobar='cmf.ManagePortal')
    #directives.read_permission(title='cmf.ManagePortal')
    total_comprobar = schema.Float(
        title=_(u"Total por comprobar"),
        required = False
    )

    notas = schema.Text(
        title = _(u'Notas'),
        required = False
    )

    
    directives.widget(
        'grupo_comprobacion',
        DataGridFieldFactory,
        pattern_options={
            'auto_append': False,
        }
    )
    grupo_comprobacion = schema.List(
        title=_(u'Comprobación'),
        description=_(u'Concepto, monto y algo más'),        
        value_type=DictRow(
            title=u"tablerow",
            schema=ITable,
        ),
        default=None,
        required=True
    )

    '''
    model.fieldset(
        'concepto',
        label=_(u"Conceptos"),
        fields=['grupo_comprobacion']
    )
    '''

    '''
    def updateWidgets(self):
        super(EditComprobacion, self).updateWidgets()        
        self.widgets['grupo_comprobacion'].auto_append = False 
    '''
class IProp(form.Schema):
    #form.widget(propietario=AjaxSelectFieldWidget)
    propietario = schema.Choice(
        __name__ = "propietario",
        title = _(u'Propietario'),
        vocabulary=u"plone.app.vocabularies.Users",
        required = True,
        default=None
    )
class AddComprobacion(add.DefaultAddForm):
    """ Default, for specific permissions only """
    portal_type = 'comprobacion'
    schema = IComprobacion
    label = u"Añadir Comprobación de gastos"
    description = u"Proporciona datos para comprobar alguno de tus gastos."    
    #additionalSchemata = [IProp] #try this later

    '''
    def updateFields(self):
        super(AddComprobacion, self).updateFields()
        #import pdb; pdb.set_trace()

        propietario = schema.Choice(
            __name__ = "propietario",
            title = _(u'Propietario'),
            vocabulary=u"plone.app.vocabularies.Users",
            required = True,
            default=None
        )
        
        field_obj = field.Fields(propietario)
        self.fields += field_obj
        #import pdb; pdb.set_trace()

        #self.fields['propietario'].widgetFactory = AjaxSelectFieldWidget

    
    def updateWidgets(self):
        super(AddComprobacion, self).updateWidgets()
        self.fields['propietario'].widgetFactory = AjaxSelectFieldWidget
    
    def datagridInitialise(self, subform, widget):
        #import pdb; pdb.set_trace()
        pass

    def datagridUpdateWidgets(self, subform, widgets, widget):
        pass
        #import pdb; pdb.set_trace()
    '''
    
    def createAndAdd(self, data):
        print("HHHHH")
        new_obj = super(AddComprobacion, self).createAndAdd(data)
        #import pdb; pdb.set_trace()
        catalog = api.portal.get_tool('portal_catalog')
        brain = catalog({'portal_type': 'comprobacion', 'id': new_obj.id})[0]
        new_obj = brain.getObject()         
        viaje = None
        if not new_obj.relacion.isBroken():            
                brains = catalog(path={'query': new_obj.relacion.to_path, 'depth': 0})
                viaje = brains[0].getObject()
        new_owner = viaje.getOwner()#api.user.get(username=).getUser()
        employee = new_owner.getId()
        #old_comp_owner = api.user.get(new_obj._owner[1]).getUser() #1
        new_obj.changeOwnership(new_owner, recursive=False)
        new_obj.setCreators([employee])
        roles = list(new_obj.get_local_roles_for_userid(employee))
        if "Owner" not in roles: roles.append("Owner")
        if "Reviewer" not in roles: roles.append("Reviewer")
        if "Manager" in roles: roles.remove("Manager")
        new_obj.manage_setLocalRoles(employee, roles)
        #new_obj.manage_setLocalRoles(old_comp_owner.getId(), ["Manager"]) #1
        new_obj.reindexObjectSecurity()
        brain = catalog({'portal_type': 'comprobacion', 'id': new_obj.id})[0]
        brain.changeOwnership(new_owner, recursive=True)
        brain.manage_setLocalRoles(employee, roles)
        brain.setCreators([employee])
        brain.reindexObjectSecurity()
        return new_obj    
    
class EditComprobacion(edit.DefaultEditForm):    
    schema = IComprobacion
    label = u"Modificar comprobaciones"
    description = u"Agregar comprobaciones."


    form.widget(
        'grupo_comprobacion',
        DataGridFieldFactory,
        pattern_options={
            'auto_append': False,
        }
    )
    #fields = field.Fields(IComprobacion)
    #fields['grupo_comprobacion'].widgetFactory = DataGridFieldFactory
    '''
    form.fieldset(
        'concepto',
        label=_(u"Conceptos"),
        fields=['grupo_comprobacion']
    )    
    '''

    #def updateFields(self):
    #    super(EditComprobacion, self).updateFields()
        #import pdb; pdb.set_trace()

    def __call__(self):
        # utility function to add resource to rendered page
        print("loading JS comprobacion")
        add_resource_on_request(self.request, 'comp_static')
        return super(EditComprobacion, self).__call__()

    def updateWidgets(self):
        #import pdb; pdb.set_trace()
        super(EditComprobacion, self).updateWidgets()        
        self.widgets['grupo_comprobacion'].auto_append = False
        #import pdb; pdb.set_trace()

    def updateActions(self):
        super(EditComprobacion, self).updateActions()
        self.actions["guardar"].addClass("context")
        self.actions["cancelar"].addClass("standalone")

    
    def datagridInitialise(self, subform, widget):
        #import pdb; pdb.set_trace()
        print("datagrid")
        #subform.fields = subform.fields.omit('importe')
        #subform.fields = subform.fields.omit('anticipo')
        '''
        if subform.fields.items():
            import pdb; pdb.set_trace()
            subform.fields['importe'].mode = 'hidden'
            subform.fields['importe'].required = False
            subform.fields['anticipo'].mode = 'hidden'
            subform.fields['anticipo'].required = False
        '''
    def datagridUpdateWidgets(self, subform, widgets, widget):
        #subform.fields = subform.fields.omit('importe')
        #subform.fields = subform.fields.omit('anticipo')
        if self.context.portal_membership.getAuthenticatedMember().getUser().has_role("Manager"):
            return
        if subform.fields.items():
            #import pdb; pdb.set_trace()
            subform.fields['importe'].mode = 'hidden'
            subform.fields['importe'].required = False
            subform.fields['anticipo'].mode = 'hidden'
            subform.fields['anticipo'].required = False
        if widgets.items():
            widgets['anticipo'].mode = 'hidden'
            widgets['anticipo'].required = False
            widgets['importe'].mode = 'hidden'
            widgets['importe'].required = False
            
    @button.buttonAndHandler(u'Guardar')
    def handleApply(self, action):
        #import pdb; pdb.set_trace()
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # Do something with valid data here
        if data.has_key("relacion"):
            temp = TemporaryRelationValue(data['relacion'].absolute_url_path()) #Una relacion no formada completamente 
            rel_full = temp.convert() 
            self.context.relacion = rel_full #tal vez deberia ser la misma aunque intente cambiarse
        if data.has_key("title"):
            self.context.tile = data['title']
        self.context.notas = data['notas']
        #self.context.grupo_comprobacion = [] if not self.context.grupo_comprobacion else self.context.grupo_comprobacion
        
        grupo_comprobacion = []
        if self.context.grupo_comprobacion == None:
            self.context.grupo_comprobacion = []

        for dicc in self.context.grupo_comprobacion:
            grupo_comprobacion.append(dicc.copy())

        
        for index, item in enumerate(data['grupo_comprobacion']):
            if index < len(grupo_comprobacion):
                if item['archivo']:
                    grupo_comprobacion[index]['archivo'] = item['archivo']
                if item['fecha']:
                    grupo_comprobacion[index]['fecha'] = item['fecha']
                if item['concepto']:
                    grupo_comprobacion[index]['concepto'] = item['concepto']
                if item['descripcion']:
                    grupo_comprobacion[index]['descripcion'] = item['descripcion']
                if item['comprobado']:
                    grupo_comprobacion[index]['comprobado'] = item['comprobado']

                #if item['anticipo']:
                #    grupo_comprobacion[index]['anticipo'] = item['anticipo']
                    
                #if item['importe']:
                #   grupo_comprobacion[index]['importe'] = item['importe']
            else:
                if not item.has_key("anticipo"):
                    item['anticipo'] = u'reembolso'
                if not item.has_key("importe"):
                    item['importe'] = 0.0
                grupo_comprobacion.append(item)

            '''    
            if item['archivo']:
                if index < len(grupo_comprobacion):
                    grupo_comprobacion[index]['archivo'] = item['archivo']
                else:
                    grupo_comprobacion.append(item)
            ''' 
        self.context.grupo_comprobacion = grupo_comprobacion
        self.status = "¡Información registrada exitosamente!"
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(u"Cancelar")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
        self.status = "Cancelado por el usuario."
        self.request.response.redirect(self.context.absolute_url())

    

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
## for validation purposes
from zope.interface import Invalid
from zope.interface import invariant
#for omissions
from z3c.form.interfaces import IEditForm

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


    fecha= schema.Date(title=u"Fecha", required=True)
    concepto = schema.TextLine(title=u"Concepto",required=True)
    descripcion = schema.TextLine(title=u"Descripción",required=True)
    importe = schema.Float(title=u"Importe",required=True)
    archivo = NamedFile(
        title=_(u'Archivo'),
        description=u"Usar comprimido para múltiples archivos.",
        required = True
    )

    directives.widget(
        'archivo',
        NamedFileFieldWidget
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
        default = None,
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

class AddComprobacion(add.DefaultAddForm):
    """ Default, for specific permissions only """
    portal_type = 'viaje'
    schema = IComprobacion

    label = u"Añadir Comprobación de gastos"
    description = u"Proporciona datos para comprobar alguno de tus gastos."


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


    def updateWidgets(self):
        #import pdb; pdb.set_trace()
        super(EditComprobacion, self).updateWidgets()
        
        self.widgets['grupo_comprobacion'].auto_append = False 

    def updateActions(self):
        super(EditComprobacion, self).updateActions()
        self.actions["guardar"].addClass("context")
        self.actions["cancelar"].addClass("standalone")
    
    @button.buttonAndHandler(u'Guardar')
    def handleApply(self, action):
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
                if item['importe']:
                    grupo_comprobacion[index]['importe'] = item['importe']
            else:
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

    

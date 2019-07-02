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
from collective.z3cform.datagridfield import DataGridFieldFactory, BlockDataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from zope import interface
from plone.app.z3cform.widget import DateFieldWidget
from plone.directives import form
from datetime import datetime
from plone.formwidget.namedfile.widget import NamedFileWidget
from zope.interface import implementer
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.browser import edit
from z3c.form import button
from z3c.relationfield import RelationValue, TemporaryRelationValue

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
    '''temporalmente lo quitamos para hacer la vista que no vulnere la seguridad por el widget'''
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
    directives.write_permission(relacion='zope2.View')
    #directives.widget(relacion=AutocompleteFieldWidget)
    relacion = RelationChoice(
        title=_(u'Solicitud'),
        source=CatalogSource(portal_type=['viaje'], review_state=['final']),#viaje_associatede,#
        required=True,
    )
    
    title = schema.TextLine(
        title=_(u'Título'),
    )
    '''
    empleado = schema.TextLine(
        title=_(u'Empleado'),
        required = True
    )
    '''
    '''
    fecha_s = schema.Datetime(
        title = _(u'Fecha creación'),
        required = True
    )
    '''
    #clave = "" unnecessary -> obj id
    
    
    notas = schema.Text(
        title = _(u'Notas'),
        required = False
    )

    '''
    archivo = NamedFile(
        title=_(u'Archivo'),
        description=u"Usar comprimido para múltiples archivos.",
        required = False
    )
    '''

    directives.widget(grupo_comprobacion=DataGridFieldFactory)
    grupo_comprobacion = schema.List(
        title=_(u'Comprobación'),
        description=_(u'Concepto, monto y algo más'),        
        value_type=DictRow(
            title=u"tablerow",
            schema=ITable,
        ),
        default = [],
        required=False
    )

    model.fieldset(
        'concepto',
        label=_(u"Conceptos"),
        fields=['grupo_comprobacion']
    )

    

class EditComprobacion(edit.DefaultEditForm):
    schema = IComprobacion
    label = u"Modificar comprobaciones"
    description = u"Agregar comprobaciones."

    '''
    def update(self):
        try:
            if self.request.REQUEST_METHOD == 'POST':
                import pdb; pdb.set_trace()
            elif self.request.REQUEST_METHOD == 'GET':
                super(EditComprobacion, self).update()
        except Exception as error:
            import pdb; pdb.set_trace()
    
    '''
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
        temp = TemporaryRelationValue(data['relacion'].absolute_url_path()) #Una relacion no formada completamente 
        rel_full = temp.convert() 
        self.context.relacion = rel_full #tal vez deberia ser la misma aunque intente cambiarse
        self.context.tile = data['title']
        self.context.notas = data['notas']
        #self.context.grupo_comprobacion = [] if not self.context.grupo_comprobacion else self.context.grupo_comprobacion
        
        grupo_comprobacion = []

        for dicc in self.context.grupo_comprobacion:
            grupo_comprobacion.append(dicc.copy())

        
        for index, item in enumerate(data['grupo_comprobacion']):
            # check if an image was submitted with each individual sponsor
            if item['archivo']:
                if index < len(grupo_comprobacion):
                    grupo_comprobacion[index]['archivo'] = item['archivo']
                else:
                    grupo_comprobacion.append(item)
                
        self.context.grupo_comprobacion = grupo_comprobacion
        self.status = "¡Información registrada exitosamente!"
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(u"Cancelar")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
        self.status = "Cancelado por el usuario."
        self.request.response.redirect(self.context.absolute_url())

    '''
    _grupo_comprobacion = None
           
    @property
    def grupo_comprobacion(self):
        print("jap")
        return self.context.grupo_comprobacion

    @grupo_comprobacion.setter
    def grupo_comprobacion(self, data):
        if data is None:
            data = []
        
        # Create a dictionary of sponsors by their oid (id)
        grupo_comprobacion = {
            v['oid']: v
            for v in (self.context.grupo_comprobacion or [])
        }
        for index, item in enumerate(data):
            # check if an image was submitted with each individual sponsor
            if not item['archivo']:
                key = item['oid']
                
                # check if the submitted id is present in the existing sponsors' id
                # if yes, store the image in the new field
                if key in grupo_comprobacion:
                    data[index]['archivo'] = grupo_comprobacion[key]['archivo']

        self.context.grupo_comprobacion = data
    '''
    

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
    archivo = schema.ASCII(
        title=_(u'Archivo'),
        description=u"Usar comprimido para múltiples archivos.",
        required = True
    )
    directives.widget(
        'archivo',
        NamedFileWidget
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
        required=False
    )

    model.fieldset(
        'concepto',
        label=_(u"Conceptos"),
        fields=['grupo_comprobacion']
    )

    
    

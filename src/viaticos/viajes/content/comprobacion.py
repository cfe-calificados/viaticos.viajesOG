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
    fecha = schema.Datetime(
        title = _(u'Fecha'),
        required = True
    )
    #clave = "" unnecessary -> obj id
    importe = schema.Float(
        title = _(u'Importe'),
        required = True,
        #min=0.0,        
        #default=0.0
    )
    
    descripcion = schema.Text(
        title = _(u'Descripción'),
        required = True
    )

    '''
    archivos = schema.List(
        title=u'Adjuntos',
        value_type=NamedFile(),
        default=1;
        required=False)

    schema.List(
            title=u'Adjuntos',
            value_type=schema.Float(),
            required=False
        )
    '''
    archivo = NamedFile(
        title=_(u'Archivo'),
        description=u"Usar comprimido para múltiples archivos.",
        required = False
    )

    fcurricula = schema.List(
        title=_(u'Concepto'),
        description=_(u'Concepto, monto y algo más'),        
        value_type=object,
        default = [0, 3, 5],
        min_length = 3,
        max_length = 3,        
        required=False,
    )

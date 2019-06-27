# -*- coding: utf-8 -*-
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
#for default purposes
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
#for access and view purposes
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm

OpcionesRequerimientos = SimpleVocabulary(
    [SimpleTerm(value=u'boleto_avion', title=_(u'Boleto de avión')),
     SimpleTerm(value=u'hospedaje', title=_(u'Hospedaje')),
     SimpleTerm(value=u'anticipo', title=_(u'Anticipo')),
     SimpleTerm(value=u'transporte_terrestre', title=_(u'Transporte terrestre')), 
     SimpleTerm(value=u'otro', title=_(u'Otro')),
    ]
)

OpcionesMotivo = SimpleVocabulary(
    [SimpleTerm(value=u'contacto', title=_(u'Contacto inicial')),
     SimpleTerm(value=u'info', title=_(u'Adquirir información')),
     SimpleTerm(value=u'propuesta', title=_(u'Propuesta comercial')),
     SimpleTerm(value=u'negociacion', title=_(u'Negociación')),
     SimpleTerm(value=u'contrato', title=_(u'Firma de contrato')),
     SimpleTerm(value=u'proceso', title=_(u'Proceso no entiendo que dice')),
     SimpleTerm(value=u'visita_tec', title=_(u'Visita técnica')),
     SimpleTerm(value=u'servicio_cliente', title=_(u'Servicio al cliente')),
     SimpleTerm(value=u'evento', title=_(u'Congreso, foro o evento especializado')),
     SimpleTerm(value=u'capacitacion', title=_(u'Capacitación')),
     SimpleTerm(value=u'otro', title=_(u'Otro')),
    ]
)

print("IViaje loaded")

class IViaje(model.Schema):
    """ Esquema dexterity para el tipo Viajes
    """

    title = schema.TextLine(
        title=_(u'Título'),
    )

    #directives.widget(motivo=RadioFieldWidget)
    motivo = schema.Choice(
        title = _(u'Motivo'),
        vocabulary = OpcionesMotivo,
        required = True        
    )    

    objetivo = RichText(
        title=_(u'Objetivo'),
        required = False
    )

    directives.widget(req=CheckBoxFieldWidget)
    """
    req = schema.Choice(
        title = _(u'Requerimientos'),
        vocabulary = OpcionesRequerimientos,
        required = True
    )
    """

    req = schema.List(title=_(u'Requerimientos'),
                               description=u"",
                               required=True,
                               value_type=schema.Choice(source=OpcionesRequerimientos),
    )

        
    fecha_salida = schema.Datetime(
        title = _(u'Fecha de salida'),
        required = True
    )

    fecha_regreso = schema.Datetime(
        title = _(u'Fecha de regreso'),
        required = True
    )

    pais = schema.TextLine(
        title = _(u'País destino'),
        required = True
    )

    ciudad = schema.TextLine(
        title = _(u'Ciudad destino'),
        required = True
    )

    cp = schema.TextLine(
        title = _(u'Código postal destino'),
        required = False
    )

    notas_avion = schema.Text(
        title = _(u'Notas del boleto de avión (?)'),
        required = False
    )

    notas_hospedaje = schema.Text(
        title = _(u'Notas del hospedaje'),
        required = False
    )

    ### datos boleto avion
    
    #directives.read_permission(tarifa='zope2.DeleteObjects')
    #directives.write_permission(tarifa='zope2.DeleteObjects')
    directives.omitted(IAddForm, 'tarifa')
    directives.omitted(IEditForm, 'tarifa')    
    tarifa = schema.Float(
        title = _(u'Tarifa'),
        required = False,
        #defaultFactory=get_context_tarifa
    )

    #directives.read_permission(aerolinea='zope2.DeleteObjects')
    #directives.write_permission(aerolinea='zope2.DeleteObjects')
    directives.omitted(IAddForm, 'aerolinea')
    directives.omitted(IEditForm, 'aerolinea')    
    aerolinea = schema.TextLine(
        title = _(u'Aerolínea'),
        required = False,
        #defaultFactory=get_context_aero
    )

    #directives.read_permission(hora_salida='zope2.DeleteObjects')
    #directives.write_permission(hora_salida='zope2.DeleteObjects')
    directives.omitted(IAddForm, 'hora_salida')
    directives.omitted(IEditForm, 'hora_salida')
    hora_salida = schema.Datetime(
        title = _(u'Hora salida'),
        required = False,
        #defaultFactory=get_context_horas
    )

    #directives.read_permission(hora_regreso='zope2.DeleteObjects')
    #directives.write_permission(hora_regreso='zope2.DeleteObjects')
    directives.omitted(IAddForm, 'hora_regreso')
    directives.omitted(IEditForm, 'hora_regreso')
    hora_regreso =  schema.Datetime(
        title = _(u'Hora regreso'),
        required = False,
        #defaultFactory=get_context_horar
    )

    #directives.read_permission(hotel_nombre='zope2.DeleteObjects')
    #directives.write_permission(hotel_nombre='zope2.DeleteObjects')
    directives.omitted(IAddForm, 'hotel_nombre')
    directives.omitted(IEditForm, 'hotel_nombre')
    hotel_nombre =  schema.TextLine(
        title = _(u'Nombre del hotel'),
        required = False,
        #defaultFactory=get_context_hotel
    )

    #directives.read_permission(hotel_domicilio='zope2.DeleteObjects')
    #directives.write_permission(hotel_domicilio='zope2.DeleteObjects')
    directives.omitted(IAddForm, 'hotel_domicilio')
    directives.omitted(IEditForm, 'hotel_domicilio')
    hotel_domicilio =  schema.Text(
        title = _(u'Domicilio del hotel'),
        required = False,
        #defaultFactory=get_context_domic
    )
           
    #import pdb; pdb.set_trace()
    
    

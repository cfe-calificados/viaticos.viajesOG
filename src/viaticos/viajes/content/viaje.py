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

    directives.widget(motivo=RadioFieldWidget)
    motivo = schema.Choice(
        title = _(u'Motivo(s)'),
        vocabulary = OpcionesMotivo,
        required = True
    )

    objetivo = RichText(
        title=_(u'Objetivo'),
        required = False
    )

    directives.widget(req=CheckBoxFieldWidget)
    req = schema.Choice(
        title = _(u'Requerimientos'),
        vocabulary = OpcionesRequerimientos,
        required = True
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
        required = True
    )

    notas_avion = schema.Text(
        title = _(u'Notas del boleto de avión (?)'),
        required = False
    )

    notas_hospedaje = schema.Text(
        title = _(u'Notas del hospedaje'),
        required = False
    )

    

# -*- coding: utf-8 -*-
"""

    Formulario para el registro de los boletos.

"""
#import pdb;pdb.set_trace()
from plone.directives import form
#from z3c import form
from zope import schema
from z3c.form import button
from viaticos.viajes import _
from Products.CMFCore.interfaces import ISiteRoot
from Products.statusmessages.interfaces import IStatusMessage
#for default purposes
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def get_context_tarifa(context):
    out = 0.0
    #import pdb; pdb.set_trace()
    try:
        out = context.tarifa
    except:
        import pdb; pdb.set_trace()
    return out 

@provider(IContextAwareDefaultFactory)
def get_context_aero(context):
    out = None
    try:
        out = context.aerolinea
    except:
        import pdb; pdb.set_trace()
    return out

@provider(IContextAwareDefaultFactory)
def get_context_horas(context):
    out = None
    try:
        out = context.hora_salida
    except:
        import pdb; pdb.set_trace()
    return out

@provider(IContextAwareDefaultFactory)
def get_context_horar(context):
    out = None
    try:
        out = context.hora_regreso
    except:
        import pdb; pdb.set_trace()
    return out

@provider(IContextAwareDefaultFactory)
def get_context_hotel(context):
    out = None
    try:
        out = context.hotel_nombre
    except:
        import pdb; pdb.set_trace()
    return out

@provider(IContextAwareDefaultFactory)
def get_context_domic(context):
    out = None
    try:
        out = context.hotel_domicilio
    except:
        import pdb; pdb.set_trace()
    return out


class ITicketForm(form.Schema):
    """ Define form fields """

    #import pdb; pdb.set_trace()
    tarifa = schema.Float(
        title=_(u'Tarifa'),
        required = True,
        min=0.0,        
        defaultFactory=get_context_tarifa
    )

    aerolinea = schema.TextLine(
        title = _(u'Aerolínea'),
        required = True,
        defaultFactory=get_context_aero
    )
    
    hora_salida = schema.Datetime(
        title = _(u'Hora salida'),
        required = True,
        defaultFactory=get_context_horas
        
    )
    
    hora_regreso =  schema.Datetime(
        title = _(u'Hora regreso'),
        required = True,
        defaultFactory=get_context_horar
    )
    
    hotel_nombre =  schema.TextLine(
        title = _(u'Nombre del hotel'),
        required = True,
        defaultFactory=get_context_hotel
    )

    hotel_domicilio =  schema.TextLine(
        title = _(u'Domicilio del hotel'),
        required = True,
        defaultFactory=get_context_domic
    )

class TicketForm(form.SchemaForm):
    """ Define Form handling

    This form can be accessed as http://yoursite/@@ticket-form

    """

    schema = ITicketForm
    ignoreContext = True

    label = u"Información de agencia"
    description = u"Agregar datos recibidos de la agencia de viajes."

    @button.buttonAndHandler(u'Aceptar')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # Do something with valid data here
        self.context.tarifa = data['tarifa']
        self.context.aerolinea = data['aerolinea']
        self.context.hora_salida = data['hora_salida']
        self.context.hora_regreso = data['hora_regreso']
        self.context.hotel_nombre = data['hotel_nombre']
        self.context.hotel_domicilio = data['hotel_domicilio']

        # Set status on this form page
        # (this status message is not bind to the session and does not go thru redirects)
        self.status = "¡Información de agencia registrada exitosamente!"
        self.request.response.redirect(self.context.absolute_url())
        #import pdb; pdb.set_trace()

    @button.buttonAndHandler(u"Cancelar")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
        self.status = "Para registrar la solicitud de gastos, es necesario capturar información de la agencia de viajes."

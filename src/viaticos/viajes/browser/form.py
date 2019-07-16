# -*- coding: utf-8 -*-
"""

    Formulario para el registro de los boletos.

"""
#import pdb;pdb.set_trace()
from plone.directives import form
#from z3c import form
from zope import schema
from z3c.form import button, field
from viaticos.viajes import _
from Products.CMFCore.interfaces import ISiteRoot
from Products.statusmessages.interfaces import IStatusMessage
#for default purposes
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
#for grouping
from plone.supermodel import model
from datetime import datetime
##for validation purposes
from zope.interface import Invalid
from zope.interface import invariant


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

    @invariant
    def validacion_horario(data):
        if data.hora_salida > data.hora_regreso:
            raise Invalid(_(u'La fecha de salida no puede ser posterior a la de regreso!'))

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

    #import pdb; pdb.set_trace()

    form.fieldset(
        'avion_req',
        label=_(u"Avión"),
        fields=['tarifa', 'aerolinea', 'hora_salida', 'hora_regreso']
    )
    
    form.fieldset(
        'hotel_req',
        label=_(u"Hospedaje"),
        fields=['hotel_nombre', 'hotel_domicilio']
    )


class TicketForm(form.SchemaForm):
    """ Define Form handling

    This form can be accessed as http://yoursite/@@ticket-form

    """

    schema = ITicketForm
    ignoreContext = True

    label = u"Información de agencia"
    description = u"Agregar datos recibidos de la agencia de viajes."

    #fields = field.Fields(ITicketForm)

    def updateFields(self):        
        super(TicketForm, self).updateFields()
        #import pdb; pdb.set_trace()
        
        group_dic = {group.__name__: group for group in self.groups}
        #for group in self.groups:
        #    group_dic[group.__name__] = group            
        if 'boleto_avion' not in self.context.req:
            avion_fields = group_dic['avion_req'].fields
            for campo in avion_fields:
                avion_fields[campo].mode = 'hidden'
                avion_fields[campo].field.required = False
            
        
        if 'hospedaje' not in self.context.req:
            hotel_fields = group_dic['hotel_req'].fields
            for campo in hotel_fields:
                hotel_fields[campo].mode = 'hidden'
                hotel_fields[campo].field.required = False

        for grupo in self.groups:
            if grupo.__name__=="avion_req" and 'boleto_avion' not in self.context.req:
                self.groups.remove(grupo)
            if grupo.__name__=="hotel_req" and 'hospedaje' not in self.context.req:
                self.groups.remove(grupo)
                
        

    @button.buttonAndHandler(u'Aceptar')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # Do something with valid data here
        if 'boleto_avion' in self.context.req:
            self.context.tarifa = data['tarifa']
            self.context.aerolinea = data['aerolinea']
            self.context.hora_salida = data['hora_salida']
            self.context.hora_regreso = data['hora_regreso']
        if 'hospedaje' in self.context.req:
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

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
#for add template purposes
from plone.dexterity.browser import add

##for validation purposes
from zope.interface import Invalid
from zope.interface import invariant

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
     SimpleTerm(value=u'proceso', title=_(u'Proceso de entrega de servicio')),
     SimpleTerm(value=u'visita_tec', title=_(u'Visita técnica')),
     SimpleTerm(value=u'servicio_cliente', title=_(u'Servicio al cliente')),
     SimpleTerm(value=u'evento', title=_(u'Congreso, foro o evento especializado')),
     SimpleTerm(value=u'capacitacion', title=_(u'Capacitación')),
     SimpleTerm(value=u'otro', title=_(u'Otro')),
    ]
)

OpcionesReserva = SimpleVocabulary(
    [SimpleTerm(value=u'reservado', title=_(u'Reservado')),
     SimpleTerm(value=u'no_reservado', title=_(u'No reservado')),
    ]
)

OpcionesPago = SimpleVocabulary(
    [SimpleTerm(value=u'pagado', title=_(u'Pagado')),
     SimpleTerm(value=u'anticipo', title=_(u'Por anticipo')),
     SimpleTerm(value=u'reembolso', title=_(u'Por reembolso')),
    ]
)

print("IViaje loaded")

class IViaje(model.Schema):
    """ Esquema dexterity para el tipo Viajes
    """

    @invariant
    def validacion_fechas(data):
        if data.fecha_salida > data.fecha_regreso:
            raise Invalid(_(u'La fecha de salida no puede ser posterior a la de regreso!'))        

    title = schema.TextLine(
        title=_(u'Título'),
    )

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

    estado = schema.TextLine(
        title = _(u'Estado destino'),
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


    directives.omitted(IAddForm, 'hotel_reserv')
    directives.omitted(IEditForm, 'hotel_reserv')    
    hotel_reserv = schema.Choice(
        title = _(u'Reservación'),
        vocabulary = OpcionesReserva,
        required = False #tmp        
    )

    directives.omitted(IAddForm, 'hotel_pago')
    directives.omitted(IEditForm, 'hotel_pago')    
    hotel_pago = schema.Choice(
        title = _(u'Pago'),
        vocabulary = OpcionesPago,
        required = False #tmp        
    )


    ### Nuevos campos ###

    ## Transporte terrestre
    directives.omitted(IAddForm, 'trans_empresa')
    directives.omitted(IEditForm, 'trans_empresa')    
    trans_empresa =  schema.TextLine(
        title = _(u'Nombre de la empresa de transporte'),
        required = True,
        #defaultFactory=get_context_hotel
    )

    directives.omitted(IAddForm, 'trans_desc')
    directives.omitted(IEditForm, 'trans_desc')    
    trans_desc =  schema.Text(
        title = _(u'Descripción'),
        required = True,
        #defaultFactory=get_context_hotel
    )    

    directives.omitted(IAddForm, 'trans_reserv')
    directives.omitted(IEditForm, 'trans_reserv')    
    trans_reserv = schema.Choice(
        title = _(u'Reservación'),
        vocabulary = OpcionesReserva,
        required = False #tmp        
    )

    directives.omitted(IAddForm, 'trans_pago')
    directives.omitted(IEditForm, 'trans_pago')    
    trans_pago = schema.Choice(
        title = _(u'Pago'),
        vocabulary = OpcionesPago,
        required = False #tmp        
    )

    ## OTRO

    directives.omitted(IAddForm, 'otro_empresa')
    directives.omitted(IEditForm, 'otro_empresa')    
    otro_empresa =  schema.TextLine(
        title = _(u'Nombre de la empresa'),
        required = True,
        #defaultFactory=get_context_hotel
    )

    directives.omitted(IAddForm, 'otro_desc')
    directives.omitted(IEditForm, 'otro_desc')    
    otro_desc =  schema.Text(
        title = _(u'Descripción'),
        required = True,
        #defaultFactory=get_context_hotel
    )    

    directives.omitted(IAddForm, 'otro_reserv')
    directives.omitted(IEditForm, 'otro_reserv')    
    otro_reserv = schema.Choice(
        title = _(u'Reservación'),
        vocabulary = OpcionesReserva,
        required = False #tmp        
    )

    directives.omitted(IAddForm, 'otro_pago')
    directives.omitted(IEditForm, 'otro_pago')    
    otro_pago = schema.Choice(
        title = _(u'Pago'),
        vocabulary = OpcionesPago,
        required = False #tmp        
    )


    ## ANTICIPO

    directives.omitted(IAddForm, 'anti_desc')
    directives.omitted(IEditForm, 'anti_desc')    
    anti_desc =  schema.Text(
        title = _(u'Descripción'),
        required = True,
        #defaultFactory=get_context_hotel
    )

    directives.omitted(IAddForm, 'anti_monto')
    directives.omitted(IEditForm, 'anti_monto')    
    anti_monto = schema.Float(
        title=_(u"Monto"),
        required=False,
        #defaultFactory=get_context_hotel
    )

    model.fieldset(
        'avion_req',
        label=_(u"Avión"),
        fields=['tarifa', 'aerolinea', 'hora_salida', 'hora_regreso']
    )
    
    model.fieldset(
        'hotel_req',
        label=_(u"Hospedaje"),
        fields=['hotel_nombre', 'hotel_domicilio', 'hotel_reserv', 'hotel_pago']
    )

    model.fieldset(
        'trans_req',
        label=_(u"Transporte terrestre"),
        fields=['trans_empresa', 'trans_desc', 'trans_reserv', 'trans_pago']
    )    

    model.fieldset(
        'otro_req',
        label=_(u"Otro"),
        fields=['otro_empresa', 'otro_desc', 'otro_reserv', 'otro_pago']
    )

    model.fieldset(
        'anticipo_req',
        label=_(u"Anticipo"),
        fields=['anti_monto' ,'anti_desc']
    )

    
from Products.CMFPlone.resources import add_resource_on_request    
class AddViaje(add.DefaultAddForm):
    def __call__(self):
        # utility function to add resource to rendered page
        #add_resource_on_request(self.request, 'exercise2')
        print("loading JS")
        add_resource_on_request(self.request, 'estaticos')
        #import pdb; pdb.set_trace()
        return super(AddViaje, self).__call__()
    
    portal_type = 'viaje'
    schema = IViaje
    label = u"Agregar solicitud de gastos"
    description = u"Añade información sobre tus salidas. "

    
class AddViajesss(add.DefaultAddView):
    form = None

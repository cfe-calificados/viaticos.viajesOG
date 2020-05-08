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
from plone.dexterity.browser import add, edit

##for validation purposes
from zope.interface import Invalid
from zope.interface import invariant
from plone import api

#for group purposes
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget, AutocompleteFieldWidget
from plone.app.z3cform.widget import AjaxSelectFieldWidget


OpcionesRequerimientos = SimpleVocabulary(
    [SimpleTerm(value=u'boleto_avion', title=_(u'Boleto de avión')),
     SimpleTerm(value=u'hospedaje', title=_(u'Hospedaje')),
     SimpleTerm(value=u'anticipo', title=_(u'Anticipo')),
     SimpleTerm(value=u'transporte_terrestre', title=_(u'Transporte terrestre')), 
     SimpleTerm(value=u'otro', title=_(u'Otro')),
    ]
)

OpcionesMotivo = SimpleVocabulary(
    [
        SimpleTerm(value=u'convenio_modificatorio', title=_(u'Convenio modificatorio')),
        SimpleTerm(value=u'contacto', title=_(u'Contacto inicial')),
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
        if ('boleto_avion' in data.req and not data.notas_avion) or ('hospedaje' in data.req and not data.notas_hospedaje) or ('transporte_terrestre' in data.req and not data.notas_transporte) or ('otro' in data.req and not data.notas_otro) :
            raise Invalid(_(u'Es necesario llenar las notas de aquellos elementos que fueron seleccionados en los requerimientos.'))

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
                      description=u"Nota: Solicitar anticipo con 48 horas de antelación a su salida seleccionada.",
                      required=False,
                      default=[],
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
        title = _(u'Notas del boleto de avión'),
        required = False
    )

    notas_hospedaje = schema.Text(
        title = _(u'Notas del hospedaje'),
        required = False
    )

    notas_transporte = schema.Text(
        title = _(u'Notas del transporte terrestre'),
        required = False
    )

    notas_otro = schema.Text(
        title = _(u'Notas del requerimiento extra'),
        description=u"Nota: Favor de especificar los montos requeridos. (Gasolina, casetas, ...)",
        required = False
    )

    directives.widget(grupo=AjaxSelectFieldWidget)
    grupo = schema.Tuple(title=_(u'Grupo'),
                         description=u"Solicitud de gastos de varios empleados. Advertencia: Una vez confirmado el borrador, solo la admón. y los superiores de los miembros del grupo podrán retirarlos de la solicitud.",
            value_type=schema.Choice(source=u"plone.app.vocabularies.Users"),
            required=False,            
            missing_value=()
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
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
class AddViaje(add.DefaultAddForm):
    ##vacio
    error_template = ViewPageTemplateFile("../browser/templates/not_allowed.pt")
    portal_type = 'viaje'
    schema = IViaje
    label = u"Agregar solicitud de gastos"
    description = u"Añade información sobre tu salida. "

    def allowed(self,user):
        """
        Regla de bloqueo nueva: No tener una comprobación abierta de más de 5 días
        """
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog.queryCatalog({"portal_type": "comprobacion", "review_state": ["bosquejo","revision"], "Creator": user.getId()})
        #import pdb; pdb.set_trace()
        return [(x.Title, x.getURL()) for x in brains]
        
    def __call__(self):
        
        current_user = self.context.portal_membership.getAuthenticatedMember()
        if not current_user.has_role("Manager") and not len(self.allowed(current_user)) < 2:
            return self.error_template()

        # utility function to add resource to rendered page
        #add_resource_on_request(self.request, 'exercise2')
        print("loading JS")
        add_resource_on_request(self.request, 'estaticos')
        #import pdb; pdb.set_trace()
        return super(AddViaje, self).__call__()
    
    
    
class EditViaje(edit.DefaultEditForm):
    schema = IViaje
    label = u"Editar solicitud de gastos "
    description = u"Modifica la información sobre tu salida."
    error_template = ViewPageTemplateFile("../browser/templates/not_editable.pt")


    def __call__(self):
        # utility function to add resource to rendered page
        #add_resource_on_request(self.request, 'exercise2')
        print("loading JS")
        add_resource_on_request(self.request, 'estaticos')
        #import pdb; pdb.set_trace()
        return super(EditViaje, self).__call__()

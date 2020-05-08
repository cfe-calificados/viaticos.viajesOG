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
import datetime as dt
##for validation purposes
from zope.interface import Invalid
from zope.interface import invariant
## para nuevos campos
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from z3c.form.browser.radio import RadioFieldWidget

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

def calc_meals(obj):
    multiplier = 1
    if obj.grupo:
        addition = 1
        if obj.getOwner().getUserName() in obj.grupo:
            addition = 0
        multiplier = len(obj.grupo)+addition            
    start_date = obj.fecha_salida
    end_date = obj.fecha_regreso
    start = start_date
    verif = [0,0,0]
    monto = 0.0
    while(start <= end_date):
        diff = (start-start_date).days
        if (start.hour, start.minute) <= (9,0) and verif[0] <= diff:
            monto += 250 * multiplier
            verif[0] += 1
        if (start.hour, start.minute) >= (9,1)  and verif[1] <= diff and (start.hour, start.minute) < (19,0):
            monto += 300 * multiplier
            verif[1] += 1
        if (start.hour, start.minute) >= (19,0) and verif[2] <= diff:
            monto += 200 * multiplier
            verif[2] += 1
        start = start + dt.timedelta(minutes=5)
    return monto

def calc_desglose(obj):
    print("here i come")
    multiplier = 1
    if obj.grupo:
        addition = 1
        if obj.getOwner().getUserName() in obj.grupo:
            addition = 0
        multiplier = len(obj.grupo)+addition
    print("wea")
    start_date = obj.fecha_salida
    end_date = obj.fecha_regreso
    start = start_date
    verif = [0,0,0]
    desglose = u""
    group = 0 #para posible agrupación en días completos de $750 (reduce lineas)
    buff = u""
    while(start <= end_date):        
        diff = (start-start_date).days
        diff_1  = (start.replace(hour=0, minute=0)-start_date.replace(hour=0, minute=0)).days+1
        #print("day:",start.strftime("%Y-%m-%d %H:%M"), "diff:", diff, "verif:", verif, "dia:", diff_1)
        if (start.hour, start.minute) <= (9,0) and verif[0] <= diff:
            #import pdb; pdb.set_trace()
            buff += u"Desayuno día "+str(diff_1)+": "+str(250*multiplier)+"\n"
            verif[0] += 1
            group += 250 
        elif (start.hour, start.minute) >= (9,1)  and verif[1] <= diff and (start.hour, start.minute) < (19,0):
            buff += u"Comida día "+str(diff_1)+": "+str(300*multiplier)+"\n"
            verif[1] += 1
            group += 300
        elif (start.hour, start.minute) >= (19,0) and verif[2] <= diff:
            buff += u"Cena día "+str(diff_1)+": "+str(200*multiplier)+"\n"
            verif[2] += 1
            group += 200            
        if group and ((start.hour, start.minute) >= (19,0) or start+dt.timedelta(minutes=5) > end_date):
            desglose += u"Comidas día "+str(diff_1)+": "+str(group*multiplier)+"\n"
            group = 0
            buff = u""
        start = start + dt.timedelta(minutes=5)
    desglose += buff
    #print(desglose)
    return desglose

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

### new functions to get defaults
@provider(IContextAwareDefaultFactory)
def get_hotel_reserv(context):
    out = None
    try:
        out = context.hotel_reserv
    except:
        import pdb; pdb.set_trace()
    return out

@provider(IContextAwareDefaultFactory)
def get_hotel_pago(context):
    out = None
    try:
        out = context.hotel_pago
    except:
        import pdb; pdb.set_trace()
    return out

@provider(IContextAwareDefaultFactory)
def get_trans_empresa(context):
    out = None
    try:
        out = context.trans_empresa
    except:
        import pdb; pdb.set_trace()
    return out

@provider(IContextAwareDefaultFactory)
def get_trans_desc(context):
    out = None
    try:
        out = context.trans_desc
    except:
        import pdb; pdb.set_trace()
    return out

@provider(IContextAwareDefaultFactory)
def get_trans_reserv(context):
    out = None
    try:
        out = context.trans_reserv
    except:
        import pdb; pdb.set_trace()
    return out

@provider(IContextAwareDefaultFactory)
def get_trans_pago(context):
    out = None
    try:
        out = context.trans_pago
    except:
        import pdb; pdb.set_trace()
    return out

@provider(IContextAwareDefaultFactory)
def get_otro_empresa(context):
    out = None
    try:
        out = context.otro_empresa
    except:
        import pdb; pdb.set_trace()
    return out

@provider(IContextAwareDefaultFactory)
def get_otro_desc(context):
    out = None
    try:
        out = context.otro_desc
    except:
        import pdb; pdb.set_trace()
    return out

@provider(IContextAwareDefaultFactory)
def get_otro_reserv(context):
    out = None
    try:
        out = context.otro_reserv
    except:
        import pdb; pdb.set_trace()
    return out

@provider(IContextAwareDefaultFactory)
def get_otro_pago(context):
    out = None
    try:
        out = context.otro_pago
    except:
        import pdb; pdb.set_trace()
    return out

@provider(IContextAwareDefaultFactory)
def get_anti_desc(context):
    out = None
    try:
        out = context.anti_desc
        if out == None:
            print("precalculando...")
            out = calc_desglose(context)
    except Exception as error:
        import pdb; pdb.set_trace()
    return out

@provider(IContextAwareDefaultFactory)
def get_anti_monto(context):
    out = None
    try:
        out = context.anti_monto
        if out == None:
            out = calc_meals(context)        
    except Exception as error:
        import pdb; pdb.set_trace()
    return out


class ITicketForm(form.Schema):
    """ Define form fields """

    @invariant
    def validacion_horario(data):
        if data.hora_salida > data.hora_regreso:
            raise Invalid(_(u'La fecha de salida no puede ser posterior a la de regreso!'))
        
    @invariant
    def validacion_anticipo(data):
        print("validacion anticipo")
        monto = 0.0
        monto_desc = 1.0
        try:
            desc = [x.split(":")[1].strip() for x in data.anti_desc.split("\n")]
            monto_desc = sum(map(float,desc))
            monto = data.anti_monto
        except ValueError as error:
            print(error)
            raise Invalid(_(u'El formato del desglose debe ser <concepto>: <monto>'))
        except IndexError as error:
            print(error)
            raise Invalid(_(u'El formato del desglose debe ser <concepto>: <monto>'))

    #import pdb; pdb.set_trace()

    ## AVION
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

    ## HOSPEDAJE
    
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

    form.widget(hotel_reserv=RadioFieldWidget)
    hotel_reserv = schema.Choice(
        title = _(u'Reservación'),
        vocabulary = OpcionesReserva,
        required = True,
        defaultFactory=get_hotel_reserv
    )

    form.widget(hotel_pago=RadioFieldWidget)
    hotel_pago = schema.Choice(
        title = _(u'Pago'),
        vocabulary = OpcionesPago,
        required = True,
        defaultFactory=get_hotel_pago
    )


    ### Nuevos campos ###

    ## Transporte terrestre
    trans_empresa =  schema.TextLine(
        title = _(u'Nombre de la empresa de transporte'),
        required = True,
        defaultFactory=get_trans_empresa
    )

    trans_desc =  schema.Text(
        title = _(u'Descripción'),
        required = True,
        defaultFactory=get_trans_desc
    )    

    form.widget(trans_reserv=RadioFieldWidget)
    trans_reserv = schema.Choice(
        title = _(u'Reservación'),
        vocabulary = OpcionesReserva,
        required = True,
        defaultFactory=get_trans_reserv
    )

    form.widget(trans_pago=RadioFieldWidget)
    trans_pago = schema.Choice(
        title = _(u'Pago'),
        vocabulary = OpcionesPago,
        required = True,
        defaultFactory=get_trans_pago
    )

    ## OTRO 
    otro_empresa =  schema.TextLine(
        title = _(u'Nombre de la empresa'),
        required = True,
        defaultFactory=get_otro_empresa
    )

    otro_desc =  schema.Text(
        title = _(u'Descripción'),
        required = True,
        defaultFactory=get_otro_desc
    )    

    form.widget(otro_reserv=RadioFieldWidget)
    otro_reserv = schema.Choice(
        title = _(u'Reservación'),
        vocabulary = OpcionesReserva,
        required = True,
        defaultFactory=get_otro_reserv
    )

    form.widget(otro_pago=RadioFieldWidget)
    otro_pago = schema.Choice(
        title = _(u'Pago'),
        vocabulary = OpcionesPago,
        required = True,
        defaultFactory=get_otro_pago
    )


    ## ANTICIPO
        
    anti_monto = schema.Float(
        title=_(u"Monto"),
        description= _(u"Total"),
        required=True,
        defaultFactory=get_anti_monto
    )
    
    anti_desc =  schema.Text(
        title = _(u'Descripción'),
        description= _(u"Desglose"),
        required = True,
        defaultFactory=get_anti_desc,        
    )


    ### GRUPOS ###
    
    form.fieldset(
        'avion_req',
        label=_(u"Avión"),
        fields=['tarifa', 'aerolinea', 'hora_salida', 'hora_regreso']
    )
    
    form.fieldset(
        'hotel_req',
        label=_(u"Hospedaje"),
        fields=['hotel_nombre', 'hotel_domicilio', 'hotel_reserv', 'hotel_pago']
    )

    form.fieldset(
        'trans_req',
        label=_(u"Transporte terrestre"),
        fields=['trans_empresa', 'trans_desc', 'trans_reserv', 'trans_pago']
    )    

    form.fieldset(
        'otro_req',
        label=_(u"Otro"),
        fields=['otro_empresa', 'otro_desc', 'otro_reserv', 'otro_pago']
    )

    form.fieldset(
        'anticipo_req',
        label=_(u"Anticipo"),
        fields=['anti_monto' ,'anti_desc']
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

        if 'transporte_terrestre' not in self.context.req:
            trans_fields = group_dic['trans_req'].fields
            for campo in trans_fields:
                trans_fields[campo].mode = 'hidden'
                trans_fields[campo].field.required = False

        if 'otro' not in self.context.req:
            otro_fields = group_dic['otro_req'].fields
            for campo in otro_fields:
                otro_fields[campo].mode = 'hidden'
                otro_fields[campo].field.required = False

        grupos_bckp = self.groups[:]
        for grupo in self.groups:
            if grupo.__name__=="avion_req" and 'boleto_avion' not in self.context.req:
                grupos_bckp.remove(grupo)
            if grupo.__name__=="hotel_req" and 'hospedaje' not in self.context.req:
                grupos_bckp.remove(grupo)                
            if grupo.__name__=="trans_req" and 'transporte_terrestre' not in self.context.req:
                grupos_bckp.remove(grupo)
            if grupo.__name__=="otro_req" and 'otro' not in self.context.req:
                grupos_bckp.remove(grupo)
        self.groups = grupos_bckp

                
        

    @button.buttonAndHandler(u'Aceptar')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        #import pdb; pdb.set_trace()

        # Do something with valid data here
        if 'boleto_avion' in self.context.req:
            self.context.tarifa = data['tarifa']
            self.context.aerolinea = data['aerolinea']
            self.context.hora_salida = data['hora_salida']
            self.context.hora_regreso = data['hora_regreso']
            
        if 'hospedaje' in self.context.req:
            self.context.hotel_nombre = data['hotel_nombre']
            self.context.hotel_domicilio = data['hotel_domicilio']
            self.context.hotel_reserv = data['hotel_reserv']
            self.context.hotel_pago = data['hotel_pago']
            
        if 'transporte_terrestre' in self.context.req:
            self.context.trans_empresa = data['trans_empresa']
            self.context.trans_desc = data['trans_desc']
            self.context.trans_reserv = data['trans_reserv']
            self.context.trans_pago = data['trans_pago']

        if 'otro' in self.context.req:
            self.context.otro_empresa = data['otro_empresa']
            self.context.otro_desc = data['otro_desc']
            self.context.otro_reserv = data['otro_reserv']
            self.context.otro_pago = data['otro_pago']

        print("handle apply")
        #Calculo del total
        self.context.anti_desc = data['anti_desc']
        desc = [x.split(":")[1].strip() for x in self.context.anti_desc.split("\n")]
        monto_desc = sum(map(float,desc))
        self.context.anti_monto = monto_desc#data['anti_monto']               
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

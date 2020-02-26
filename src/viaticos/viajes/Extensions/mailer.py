# -*- coding: utf-8 -*- 
import os
from plone import api
import ast
import locale
from plone.app.textfield.interfaces import ITransformer
import socket
import datetime as dt

""" Get name of SERVER """
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
URL="http://"+s.getsockname()[0]+":8080/"#"http://viaticos.cfecalificados.mx:8080/"
s.close()



def get_bosses(username, grupo):
    #import pdb; pdb.set_trace()
    membership = api.portal.get_tool('portal_membership')
    downward = membership.getMemberById(username).getProperty("downward")
    downward_dic = {}
    try:
        downward_dic = ast.literal_eval(downward)
    except SyntaxError:
        print("Missing hierarchy for "+username)
        
    for employee in grupo:
        tmp = {}
        downward = membership.getMemberById(employee).getProperty("downward")
        try:
            tmp = ast.literal_eval(downward)
        except SyntaxError:
            print("Missing hierarchy for "+employee)            
            downward_dic.update(tmp)
    return downward_dic

def complete(reqs):
    trade = {"boleto_avion": u"vuelo", "hospedaje":u"hospedaje", "anticipo":u"viáticos", "transporte_terrestre":u"transporte terrestre", "otro":u"entre otros"}
    return [trade[x] for x in reqs]

def complete_m(motivo):
    trade = {"convenio_modificatorio": "un convenio modificatorio", "contacto":u"el contacto inicial con un cliente", "info":u"una adquisición de información", "propuesta":u"una propuesta comercial", "negociacion":u"una negociación", "contrato":u"una firma de contrato", "proceso":u"un proceso de entrega de servicio", "visita_tec":u"una visita técnica", "servicio_cliente":u"una visita de servicio al cliente", "evento":u"una asistencia a un congreso, foro o evento especializado", "capacitacion":u"una capacitación", "otro":u"un requerimiento de su área"}
    return trade[motivo]
    
def build_body(brain, owner):
    transformer = ITransformer(brain)
    #owner = users.getUserById(brain.owner_info()['id'])
    #import pdb; pdb.set_trace()
    locale.setlocale(locale.LC_TIME, 'es_MX.utf-8')
    body = u"Viajes Turísticos Arcoíris\nPresente\n\n\nPor medio del presente agradecemos se realice la siguiente cotización:\n\n"
    body += u"Vuelo\nDestino: "+brain.ciudad.encode('utf-8').decode('utf-8')+u", "+brain.estado.encode('utf-8').decode('utf-8')+u", "+brain.pais.encode('utf-8').decode('utf-8')+u"\nMotivo: "+complete_m(brain.motivo).capitalize()+u"\nFecha de salida: "+brain.fecha_salida.strftime("%A %d de %B de %Y").decode('utf-8').capitalize()+u"\nFecha de regreso: "+brain.fecha_regreso.strftime("%A %d de %B de %Y").decode('utf-8').capitalize()+u"\nNombre: "+owner.getProperty("fullname").decode('utf-8')+u"\nÁrea de adscripción: "+owner.getProperty("coordinacion").capitalize()+u"\n\nNotas de avión:\n"+brain.notas_avion.encode('utf-8').decode('utf-8')+u"\n\n" if 'boleto_avion' in brain.req else ""
    body += u"Hospedaje\nCaracterísticas: "+brain.notas_hospedaje.encode('utf-8').decode('utf-8')+u"\n\n" if 'hospedaje' in brain.req else ""     
    body += u"Transportación terrestre\nEspecificaciones: "+brain.notas_transporte.encode('utf-8').decode('utf-8')+u"\n\n" if 'transporte_terrestre' in brain.req else "" 
    body += u"Otros\nEspecificaciones: "+brain.notas_otro.encode('utf-8').decode('utf-8')+u"\n\n" if 'otro' in brain.req else ""    
    body += u"Finalmente, la cotización deberá enviarse a los siguientes correos electrónicos: "+owner.getProperty("email").decode('utf-8')+u"; administracion@calificados.cfe.mx; cesar.banos@calificados.cfe.mx; zulema.osorio@calificados.cfe.mx\n\n"
    body += u"En caso de cualquier duda o comentario favor de comunicarse con Zulema Osorio Amarillas al teléfono 4123 5411.\n\n"
    body += u"Atentamente\nAdministración\ncfe_calificados"
    agency_body = body
    
    out = u"Estimado Coordinador,\n\nLe comunicamos que "+owner.getProperty("fullname").decode('utf-8')+u" ha solicitado: "+u", ".join(complete(brain.req))+u" para acudir el día "+brain.fecha_salida.strftime("%A %d de %B de %Y").decode('utf-8')+u" a la ciudad de "+brain.ciudad.encode('utf-8').decode('utf-8')+u", "+brain.pais.encode('utf-8').decode('utf-8')+u", para realizar "+complete_m(brain.motivo)+u". "+(u"Objetivo: "+transformer(brain.objetivo, 'text/plain') if brain.objetivo else "")+u"\n\n" 
    out += u"Por lo anterior, mucho agradeceremos que, en caso de no haber autorizado dicha visita, se notifique a esta dirección su negativa "+URL+brain.virtual_url_path()+u", o en su caso, comunicarse con Zulema Osorio Amarillas a la extensión 21411.\n\n\n\nAtentamente\nAdministración\ncfe_calificados\n"
    bosses_body = out
    '''
    out += u"\nTítulo: "+brain.title.encode('utf-8').decode('utf-8')
    out += u"\nMotivo: "+brain.motivo.encode('utf-8').decode('utf-8')
    out += u"\nRequerimientos: "
    out += u"\nFecha de salida: "+brain.fecha_salida.strftime("%A %d %B %Y")
    out += u"\nFecha de regreso: "+brain.fecha_regreso.strftime("%A %d %B %Y")
    out += u"\nPaís destino: "+brain.pais.encode('utf-8').decode('utf-8')
    out += u"\nCiudad destino: "+brain.ciudad.encode('utf-8').decode('utf-8')+(" CP: "+brain.cp.encode('utf-8').decode('utf-8') if brain.cp else "")
    '''
    
    return agency_body, bosses_body
    
    
def boss_mail(self, state_change):
    print("borrador cambio")
    #import pdb; pdb.set_trace()
    #uf = state_change.getPortal().acl_users

    membership = api.portal.get_tool('portal_membership')
    obj_owner = membership.getMemberById(state_change.object.owner_info()['id'])
    downward = obj_owner.getProperty("downward")
    downward_dic = {}
    try:
        downward_dic = ast.literal_eval(downward)
    except SyntaxError:
        print("Missing hierarchy for "+obj_owner.getUserName())
    grupo = state_change.object.grupo
    if grupo:        
        downward_dic = get_bosses(obj_owner.getUserName(), grupo)
    
    agency_mail,boss_mail = build_body(state_change.object,obj_owner)
    receivers = []#+["administracion@calificados.cfe.mx", "cesar.banos@calificados.cfe.mx", "zulema.osorio@calificados.cfe.mx"]
    
    for boss in downward_dic:
        jefe = membership.getMemberById(boss)
        receivers.append(jefe.getProperty("email"))

    ## Envio correo coordinador
    api.portal.send_email(
        recipient=";".join(receivers),
        sender="noreply@plone.org",
        subject=u"Solicitud de gastos: "+state_change.object.title.encode('utf-8').decode('utf-8'),
        body=boss_mail,
    )

    # Envio correo agencia
    if 'boleto_avion' in state_change.object.req or 'hospedaje' in state_change.object.req: 
        api.portal.send_email(
            recipient="agencia_viajes@foo.com",#+";administracion@calificados.cfe.mx;cesar.banos@calificados.cfe.mx; zulema.osorio@calificados.cfe.mx",   
            sender="noreply@plone.org",
            subject=u"Solicitud de cotización",
            body=agency_mail,
        )


def agency_mail(self, state_change):
    print("enviando correo a la compañía de viajes")
    membership = api.portal.get_tool('portal_membership')
    obj_owner = membership.getMemberById(state_change.object.owner_info()['id'])
    agency_mail,boss_mail = build_body(state_change.object,obj_owner)
    if 'boleto_avion' in state_change.object.req or 'hospedaje' in state_change.object.req: 
        api.portal.send_email(
            recipient="agencia_viajes@foo.com",#+";administracion@calificados.cfe.mx;cesar.banos@calificados.cfe.mx; zulema.osorio@calificados.cfe.mx",   
            sender="noreply@plone.org",
            subject=u"Solicitud de cotización",
            body=agency_mail,
        )
        #import pdb; pdb.set_trace()


def return_to_draft(self, state_change):    
    membership = api.portal.get_tool('portal_membership')
    trip = state_change.object
    body = u"Estimado usuario,\n se le informa por este medio que su solicitud de gastos con título: '"+trip.title.encode('utf-8').decode('utf-8')+u"' no fue aprobada por la administración o su autorizador. Favor de hacer las ediciones pertinentes antes de confirmar su solicitud. "+URL+state_change.object.virtual_url_path()
    body2 = u"Estimado usuario,\n se le informa por este medio que su solicitud de gastos con título: '"+trip.title.encode('utf-8').decode('utf-8')+u"' no fue aprobada por la administración o su autorizador. Favor de hacer las ediciones pertinentes antes de confirmar su solicitud."
    obj_owner = membership.getMemberById(trip.owner_info()['id'])
    receivers = []
    if trip.grupo:
        receivers = [x for x in trip.grupo if x != trip.owner_info()['id']]#+([trip.owner_info()['id']] if trip.owner_info()['id'] not in trip.grupo else [])
        api.portal.send_email(
            recipient=";".join([membership.getMemberById(x).getProperty("email") for x in receivers]),   
            sender="noreply@plone.org",
            subject=u"Solicitud de gastos no aprobada",
            body=body,
        )
    # Envio de rechazo al usuario solicitante
    api.portal.send_email(
        recipient=obj_owner.getProperty("email"),#+";administracion@calificados.cfe.mx; cesar.banos@calificados.cfe.mx; zulema.osorio@calificados.cfe.mx",      
        sender="noreply@plone.org",
        subject=u"Solicitud de gastos rechazada",
        body=body2,
    )

    # Envio correo agencia
    if 'boleto_avion' in state_change.object.req or 'hospedaje' in state_change.object.req:
        agency_mail = u"Viajes Turísticos Arcoíris\nPresente\n\nPor medio del presente agradecemos se realice la cancelación de la cotización número: (NÚMERO).\n\nPara cualquier duda o comentario comunicarse con Zulema Osorio Amarillas a la extensión 21411.\n\n\nAtentamente\n\nAdministración cfe_calificados"
        api.portal.send_email(
            recipient="agencia_viajes@foo.com",#+";administracion@calificados.cfe.mx; cesar.banos@calificados.cfe.mx; zulema.osorio@calificados.cfe.mx",   
            sender="noreply@plone.org",
            subject=u"Solicitud de cotización",
            body=agency_mail,
        )
    

def rejected(self, state_change):    
    membership = api.portal.get_tool('portal_membership')
    trip = state_change.object
    #"No se pudieron satisfacer los requerimientos de su solicitud. Favor de acercarse a la administración..."
    body = u"Estimado usuario,\n se le informa por este medio que su solicitud de gastos con título: '"+trip.title.encode('utf-8').decode('utf-8')+u"' no concluyó con éxito su trámite. Favor de hacer las ediciones pertinentes antes de comenzar de nuevo el proceso de solicitud. "+URL+state_change.object.virtual_url_path()
    body2 = u"Estimado usuario,\n se le informa por este medio que su solicitud de gastos con título: '"+trip.title.encode('utf-8').decode('utf-8')+u"' no concluyó con éxito su trámite. Favor de realizar las ediciones pertinentes antes de comenzar de nuevo el proceso de solicitud."
    obj_owner = membership.getMemberById(trip.owner_info()['id'])
    receivers = []
    bosses = []
    
    downward = obj_owner.getProperty("downward")
    downward_dic = {}
    try:
        downward_dic = ast.literal_eval(downward)
    except SyntaxError:
        print("Missing hierarchy for "+obj_owner.getUserName())
    grupo = state_change.object.grupo
    if trip.grupo:        
        downward_dic = get_bosses(obj_owner.getUserName(), grupo)    


    for boss in downward_dic:
        jefe = membership.getMemberById(boss)
        bosses.append(jefe.getProperty("email"))
        
        
    if trip.grupo:
        receivers = [x for x in trip.grupo if x != trip.owner_info()['id']]#+([trip.owner_info()['id']] if trip.owner_info()['id'] not in trip.grupo else [])
        api.portal.send_email(
            recipient=";".join([membership.getMemberById(x).getProperty("email") for x in receivers]+bosses),   
            sender="noreply@plone.org",
            subject=u"Solicitud de gastos rechazada",
            body=body2,
        )


    api.portal.send_email(
        recipient=";".join([obj_owner.getProperty("email")]+bosses),   
        sender="noreply@plone.org",
        subject=u"Solicitud de gastos rechazada",
        body=body,
    )

    # Envio correo agencia
    if 'boleto_avion' in state_change.object.req or 'hospedaje' in state_change.object.req:
        agency_mail = u"Viajes Turísticos Arcoíris\nPresente\n\nPor medio del presente agradecemos se realice la cancelación de la cotización número: (NÚMERO).\n\nPara cualquier duda o comentario comunicarse con Zulema Osorio Amarillas a la extensión 21411.\n\n\nAtentamente\n\nAdministración cfe_calificados"
        api.portal.send_email(
            recipient="agencia_viajes@foo.com",#+";administracion@calificados.cfe.mx; cesar.banos@calificados.cfe.mx; zulema.osorio@calificados.cfe.mx",   
            sender="noreply@plone.org",
            subject=u"Solicitud de cotización",
            body=agency_mail,
        )
    

def comp_save(self, state_change):
    comp = state_change.object
    membership = api.portal.get_tool('portal_membership')
    obj_owner = membership.getMemberById(comp.owner_info()['id'])
    body = u"Estimado Coordinador,\n\nLe comunicamos que "+obj_owner.getProperty("fullname").decode('utf-8')+u" ha solicitado la revisión de: "+comp.title.encode('utf-8').decode('utf-8')+u". Favor de dirigirse a "+URL+state_change.object.virtual_url_path()+u" para visualizar la información."

    downward = obj_owner.getProperty("downward")
    downward_dic = {}
    try:
        downward_dic = ast.literal_eval(downward)
    except SyntaxError:
        print("Missing hierarchy for "+obj_owner.getUserName())

    receivers = []
    for boss in downward_dic:
        jefe = membership.getMemberById(boss)
        receivers.append(jefe.getProperty("email"))
        
    api.portal.send_email(
        recipient=";".join(receivers),   
        sender="noreply@plone.org",
        subject=comp.title.encode('utf-8').decode('utf-8'),
        body=body,
    )

def comp_reg(self, state_change):
    comp = state_change.object
    membership = api.portal.get_tool('portal_membership')
    obj_owner = membership.getMemberById(comp.owner_info()['id'])
    body = u"Estimado usuario,\n\nLe comunicamos que su "+comp.title.encode('utf-8').decode('utf-8')+u" fue aprobada. Favor de dirigirse a "+URL+state_change.object.virtual_url_path()+u" para visualizar la información."        
    api.portal.send_email(
    recipient=obj_owner.getProperty("email"),   
        sender="noreply@plone.org",
        subject=u"Aprobada: "+comp.title.encode('utf-8').decode('utf-8'),
        body=body,
    )


def comp_fail(self, state_change):
    comp = state_change.object
    membership = api.portal.get_tool('portal_membership')
    obj_owner = membership.getMemberById(comp.owner_info()['id'])
    body = u"Estimado usuario,\n\nLe comunicamos que su "+comp.title.encode('utf-8').decode('utf-8')+u" no fue aprobada. Favor de dirigirse a "+URL+state_change.object.virtual_url_path()+u" para hacer los cambios pertinentes y volver a intentarlo nuevamente."    
    api.portal.send_email(
        recipient=obj_owner.getProperty("email"),   
        sender="noreply@plone.org",
        subject=u"Rechazada: "+comp.title.encode('utf-8').decode('utf-8'),
        body=body,
    )


def finances_mail(self, state_change):
    print("se envía correo a finanzas")
    #import pdb; pdb.set_trace()
    trip = state_change.object
    membership = api.portal.get_tool('portal_membership')
    obj_owner = membership.getMemberById(trip.owner_info()['id'])
    body = u"Coordinación de Finanzas\nPresente\n\nPor medio del presente agradecemos se realice el depósito de anticipo por un monto de "+str(trip.anti_monto)+u" con motivo de:\n\n"+trip.anti_desc+u"\n\n\nEn caso de rechazar la solicitud favor de dar clic en el siguiente link "+URL+state_change.object.virtual_url_path()+u".\n\n\nPara cualquier duda o comentario comunicarse con Zulema Osorio Amarillas a la extensión 21411.\n\nAtentamente\n\nAdministración\n\ncfe_calificados"        
    api.portal.send_email(
        recipient="finanzas@foo.com", #liliana.garcia@calificados.cfe.mx   
        sender="noreply@plone.org",
        subject=u"Anticipo pendiente de aprobación: "+trip.title.encode('utf-8').decode('utf-8'),
        body=body,
    )

def finances_rejected(self, state_change):
    print("se envía correo a admon. de no autorización de anticipo")
    trip = state_change.object
    membership = api.portal.get_tool('portal_membership')
    obj_owner = membership.getMemberById(trip.owner_info()['id'])
    body = u"Coordinación de Administración\nPresente\n\nPor medio del presente le comunicamos que se rechazó la solicitud de anticipo por un monto de "+str(trip.anti_monto)+u" con motivo de:\n\n"+trip.anti_desc+u"\n\nPara revisar la información de la solicitud, pruebe visitar el siguiente enlace: "+URL+state_change.object.virtual_url_path()+u"\n\nPara cualquier duda o comentario comunicarse con Liliana Garcia a la extensión 21411.\n\nAtentamente\n\nAdministración\ncfe_calificados"
    api.portal.send_email(
    recipient="finanzas@foo.com", #administracion@calificados.cfe.mx; cesar.banos@calificados.cfe.mx; zulema.osorio@calificados.cfe.mx 
        sender="noreply@plone.org",
        subject=u"Anticipo rechazado: "+trip.title.encode('utf-8').decode('utf-8'),
        body=body,
    )


def implant_mail(self, state_change):
    print("se envía correo a implant solicitando depósito de anticipo. También a usuario con montos aceptados de su comprobación.")


def implant_comp(self, state_change):
    print("Se envía correo a implant solicitando carga de facturas de hospedaje y vuelo.")

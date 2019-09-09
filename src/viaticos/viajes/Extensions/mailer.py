# -*- coding: utf-8 -*- 
import os
from plone import api
import ast
import locale
from plone.app.textfield.interfaces import ITransformer

def complete(reqs):
    trade = {"boleto_avion": u"vuelo", "hospedaje":u"hospedaje", "anticipo":u"viáticos", "transporte_terrestre":u"transporte terrestre", "otro":u"entre otros"}
    return [trade[x] for x in reqs]

def complete_m(motivo):
    trade = {"contacto":u"el contacto inicial con un cliente", "info":u"una adquisición de información", "propuesta":u"una propuesta comercial", "negociacion":u"una negociación", "contrato":u"una firma de contrato", "proceso":u"un proceso de entrega de servicio", "visita_tec":u"una visita técnica", "servicio_cliente":u"una visita de servicio al cliente", "evento":"una asistencia a un congreso, foro o evento especializado", "capacitacion":"una capacitación", "otro":"un requerimiento de su área"}
    return trade[motivo]
    
def build_body(brain, owner):
    transformer = ITransformer(brain)
    #owner = users.getUserById(brain.owner_info()['id'])
    #import pdb; pdb.set_trace()
    locale.setlocale(locale.LC_TIME, 'es_MX.utf-8')
    body = u"Viajes Turísticos Arcoíris\nPresente\n\n\nPor medio del presente agradecemos se realice la siguiente cotización:\n\n"
    body += u"Vuelo\nDestino: "+brain.ciudad.encode('utf-8').decode('utf-8')+u", "+brain.estado.encode('utf-8').decode('utf-8')+u", "+brain.pais.encode('utf-8').decode('utf-8')+u"\nMotivo: "+complete_m(brain.motivo)+u"\nFecha de salida: "+brain.fecha_salida.strftime("%A %d de %B de %Y")+u"\nFecha de regreso: "+brain.fecha_regreso.strftime("%A %d de %B de %Y")+u"\nNombre: "+owner.getProperty("fullname").decode('utf-8')+u"\nÁrea de adscripción:Eh?\nNotas: "+brain.notas_avion.encode('utf-8').decode('utf-8')+u"\n\n" if 'boleto_avion' in brain.req else ""
    body += u"Hospedaje\nCaracterísticas: "+brain.notas_hospedaje.encode('utf-8').decode('utf-8')+u"\n\n" if 'hospedaje' in brain.req else ""     
    body += u"Transportación terrestre\nEspecificaciones: "+brain.notas_transporte.encode('utf-8').decode('utf-8')+u"\n\n" if 'transporte_terrestre' in brain.req else "" 
    body += u"Otros\nEspecificaciones: "+brain.notas_otro.encode('utf-8').decode('utf-8')+u"\n\n" if 'otro' in brain.req else ""    
    body += u"Finalmente, la cotización deberá enviarse a los siguientes correos electrónicos: "+owner.getProperty("email").decode('utf-8')+u"; administracion@calificados.cfe.mx; cesar.banos@calificados.cfe.mx; zulema.osorio@calificados.cfe.mx\n\n"
    body += u"En caso de cualquier duda o comentario favor de comunicarse con Zulema Osorio Amarillas al teléfono 4123 5411.\n\n"
    body += u"Atentamente\nAdministración\ncfe_calificados"
    agency_body = body
    
    out = u"Estimado Coordinador,\n\nLe comunicamos que "+owner.getProperty("fullname").decode('utf-8')+u" ha solicitado: "+u", ".join(complete(brain.req))+u" para acudir el día "+brain.fecha_salida.strftime("%A %d de %B de %Y")+u" a la ciudad de "+brain.ciudad.encode('utf-8').decode('utf-8')+u", "+brain.pais.encode('utf-8').decode('utf-8')+u", para realizar "+complete_m(brain.motivo)+u". "+(u"Objetivo: "+transformer(brain.objetivo, 'text/plain') if brain.objetivo else "")+u"\n\n" 
    out += u"Por lo anterior, mucho agradeceremos que, en caso de no haber autorizado dicha visita, se notifique a esta dirección su negativa <link>, o en su caso, comunicarse con Zulema Osorio Amarillas a la extensión 21411.\n\n\n\nAtentamente\nAdministración\ncfe_calificados\n"
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
    
    
def test_user(self, state_change):
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
        print("Missing hierarchy for "+username)
    
    agency_mail,boss_mail = build_body(state_change.object,obj_owner)
    for boss in downward_dic:
        jefe = membership.getMemberById(boss)
        #pass
        api.portal.send_email(
            recipient=jefe.getProperty("email"),   
            sender="noreply@plone.org",
            subject="Prueba",
            body=boss_mail,
        )


def test(self, state_change):
    print("enviando correo a la compañía")
    membership = api.portal.get_tool('portal_membership')
    obj_owner = membership.getMemberById(state_change.object.owner_info()['id'])
    agency_mail,boss_mail = build_body(state_change.object,obj_owner)
    if 'boleto_avion' in state_change.object.req or 'hospedaje' in state_change.object.req: 
        api.portal.send_email(
            recipient="dummy@foo.com",   
            sender="noreply@plone.org",
            subject="Prueba",
            body=agency_mail,
        )
        #import pdb; pdb.set_trace()


def return_to_draft(self, state_change):    
    membership = api.portal.get_tool('portal_membership')
    trip = state_change.object
    body = u"Estimado usuario,\n se le informa mediante este medio que su solicitud de gastos con título: '"+trip.title.encode('utf-8').decode('utf-8')+u"' no fue aprobada por la administración o su autorizador. Favor de hacer las ediciones pertinentes antes de confirmar su solicitud. <link>"
    obj_owner = membership.getMemberById(trip.owner_info()['id'])
    receivers = []
    if trip.grupo:
        receivers = [x for x in trip.grupo]+([trip.owner_info()['id']] if trip.owner_info()['id'] not in trip.grupo else [])
    else:
        receivers.append(trip.owner_info()['id'])
    for x in receivers:
        usuario = membership.getMemberById(x)
        api.portal.send_email(
            recipient=usuario.getProperty("email"),   
            sender="noreply@plone.org",
            subject="Solicitud de gastos no aprobada",
            body=body,
        )

def rejected(self, state_change):    
    membership = api.portal.get_tool('portal_membership')
    trip = state_change.object
    body = u"Estimado usuario,\n se le informa mediante este medio que su solicitud de gastos con título: '"+trip.title.encode('utf-8').decode('utf-8')+u"' no concluyó con éxito su trámite. Favor de hacer las ediciones pertinentes antes de comenzar de nuevo el proceso de solicitud. <link>"
    obj_owner = membership.getMemberById(trip.owner_info()['id'])
    receivers = []
    if trip.grupo:
        receivers = [x for x in trip.grupo]+([trip.owner_info()['id']] if trip.owner_info()['id'] not in trip.grupo else [])
    else:
        receivers.append(trip.owner_info()['id'])
    for x in receivers:
        usuario = membership.getMemberById(x)
        api.portal.send_email(
            recipient=usuario.getProperty("email"),   
            sender="noreply@plone.org",
            subject="Solicitud de gastos rechazada",
            body=body,
        )

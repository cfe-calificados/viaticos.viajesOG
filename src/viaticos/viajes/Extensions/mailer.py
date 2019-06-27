# -*- coding: utf-8 -*- 
import os
from plone import api


def test(self, state_change):
    os.system("ls")
    print("hola, este es un test para enviar correo a la compañía")
    #import pdb; pdb.set_trace()

def build_body(brain, users):
    owner = users.getUserById(brain.owner_info()['id'])
    out = u"El usuario "+owner.getProperty("fullname").encode('utf-8').decode('utf-8')+" acaba de registrar una nueva solicitud de gastos:\n\n"
    out += u"\nTítulo: "+brain.title.encode('utf-8').decode('utf-8')
    out += u"\nMotivo: "+brain.motivo.encode('utf-8').decode('utf-8')
    out += u"\nRequerimientos: "
    out += u"\nFecha de salida: "+brain.fecha_salida.strftime("%A %d %B %Y")
    out += u"\nFecha de regreso: "+brain.fecha_regreso.strftime("%A %d %B %Y")
    out += u"\nPaís destino: "+brain.pais.encode('utf-8').decode('utf-8')
    out += u"\nCiudad destino: "+brain.ciudad.encode('utf-8').decode('utf-8')+" CP: "+brain.cp.encode('utf-8').decode('utf-8')
    return out
    
    
def test_user(self, state_change):
    print("borrador cambio")
    #import pdb; pdb.set_trace()
    uf = state_change.getPortal().acl_users
    body_builded = build_body(state_change.object,uf)
    readers = [x for x in uf.getUsers() if x.has_role("Reader")]
    for boss in readers:
        api.portal.send_email(
            recipient=boss.getProperty("email"),   
            sender="noreply@plone.org",
            subject="Prueba",
            body=body_builded,
        )

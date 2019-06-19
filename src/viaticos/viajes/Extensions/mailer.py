# -*- coding: utf-8 -*- 
import os
from plone import api


def test(self, state_change):
    os.system("ls")
    print("hola, este es un test para enviar correo a la compañía")
    #import pdb; pdb.set_trace()

def build_body(brain, users):
    owner = users.getUserById(brain.owner_info()['id'])
    out = "El usuario "+owner.getProperty("fullname")+" acaba de registrar una nueva solicitud de gastos:\n\n"
    out += u"\nTítulo: "+brain.title
    out += u"\nMotivo: "+brain.motivo
    out += u"\nRequerimientos: "
    out += u"\nFecha de salida: "+brain.fecha_salida.strftime("%A %d %B %Y")
    out += u"\nFecha de regreso: "+brain.fecha_regreso.strftime("%A %d %B %Y")
    out += u"\nPaís destino: "+brain.pais
    out += u"\nCiudad destino: "+brain.ciudad+" CP: "+brain.cp
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

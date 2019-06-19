# -*- coding: utf-8 -*- 
import os
from plone import api
from datetime import datetime

def create_comprobacion(self, state_change):
    portal = api.portal.get()
    obj = None#api.content.create(safe_id=True,type="viaje", title="Hola", motivo="contacto", req=["boleto_avion"], fecha_salida=datetime(2019,1,1), fecha_regreso=datetime(2019,1,2), pais="MExico", ciudad="Ciudad", cp="2222", container=portal.viaticos)
    if obj != None:
        print("We made it!")
    else:
        print("Algo malo pasó")

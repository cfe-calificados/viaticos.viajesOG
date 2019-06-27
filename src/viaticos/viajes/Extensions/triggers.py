# -*- coding: utf-8 -*- 
import os
from plone import api
from datetime import datetime

def create_comprobacion(self, state_change):
    portal = api.portal.get()
    trip = state_change.object
    obj = None    
    try:
        obj = api.content.create(safe_id=True,type="comprobacion", relacion=trip, title=u"Comprobación de "+trip.title.encode('utf-8').decode('utf-8'), fecha=datetime.now(), importe=0, descripcion=u"Descripción", archivo=None, container=portal.viaticos) #None#
    except Exception as error:
        import pdb; pdb.set_trace()
    if obj != None:
        print("We made it!")
    else:
        print("Algo malo pasó")

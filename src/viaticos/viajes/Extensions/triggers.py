# -*- coding: utf-8 -*- 
import os
from plone import api
from datetime import datetime
from z3c.relationfield import RelationValue, TemporaryRelationValue
from plone.uuid.interfaces import IUUID

def create_comprobacion(self, state_change):
    portal = api.portal.get()
    trip = state_change.object
    obj = None
    #trip_ctx = trip.aq_base
    #uuid = IUUID(trip_ctx)    
    temp = TemporaryRelationValue(trip.absolute_url_path()) #Una relacion no formada completamente 
    rel_full = temp.convert() 

    try:
        obj = api.content.create(safe_id=True,type="comprobacion", relacion=rel_full, title=u"Comprobación de "+trip.title.encode('utf-8').decode('utf-8'), notas=u"", grupo_comprobacion=[{'descripcion': u'Descripción', 'fecha': datetime.now(), 'concepto': u'Concepto', 'importe': 0.0, 'archivo': None}], container=portal.viaticos)#api.content.create(safe_id=True,type="comprobacion", relacion=trip, title=u"Comprobación de "+trip.title.encode('utf-8').decode('utf-8'), fecha=datetime.now(), importe=0, descripcion=u"Descripción", archivo=None, container=portal.viaticos) #None#
    except Exception as error:
        import pdb; pdb.set_trace()
    if obj != None:
        print("We made it!")
    else:
        print("Algo malo pasó")

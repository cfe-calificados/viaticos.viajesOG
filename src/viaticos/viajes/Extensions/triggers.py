# -*- coding: utf-8 -*- 
import os
from plone import api
from datetime import datetime
from z3c.relationfield import RelationValue, TemporaryRelationValue
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName

def generate(viaje):
    desc_monto = [[elem.strip() for elem in x.split(":")] for x in viaje.anti_desc.split("\n")]
    grupo = []
    for x in desc_monto:
        #import pdb; pdb.set_trace()
        grupo.append({'descripcion': u'Descripción', 'fecha': datetime.now(), 'concepto': x[0], 'importe': float(x[1]), 'archivo': None, 'comprobado':0.0, 'anticipo':u'si'})
    return grupo#[{'descripcion': u'Descripción', 'fecha': datetime.now(), 'concepto': u'Concepto', 'importe': 0.0, 'archivo': None}]

def create_comprobacion(self, state_change):
    portal = api.portal.get()
    trip = state_change.object
    obj = None
    #trip_ctx = trip.aq_base
    #uuid = IUUID(trip_ctx)    
    temp = TemporaryRelationValue(trip.absolute_url_path()) #Una relacion no formada completamente 
    rel_full = temp.convert() 

    try:
        obj = api.content.create(safe_id=True,type="comprobacion", relacion=rel_full, title=u"Comprobación de "+trip.title.encode('utf-8').decode('utf-8'), total_comprobar=trip.anti_monto,notas=u"", grupo_comprobacion=generate(trip), container=portal.viaticos)#api.content.create(safe_id=True,type="comprobacion", relacion=trip, title=u"Comprobación de "+trip.title.encode('utf-8').decode('utf-8'), fecha=datetime.now(), importe=0, descripcion=u"Descripción", archivo=None, container=portal.viaticos) #None#
    except Exception as error:
        import pdb; pdb.set_trace()
    if obj != None:
        print("We made it!")
        #import pdb; pdb.set_trace()
        try:
            trip_owner = trip.getOwner()
            old_comp_owner = obj.getOwner() #1
            obj.changeOwnership(trip_owner, recursive=False)
            obj.setCreators([trip.getOwner().getId()])
            roles = list(obj.get_local_roles_for_userid(trip.getOwner().getId()))
            if "Owner" not in roles: roles.append("Owner")
            if "Reviewer" not in roles: roles.append("Reviewer")
            if "Manager" in roles: roles.remove("Manager")
            obj.manage_setLocalRoles(trip.getOwner().getId(), roles)
            obj.manage_setLocalRoles(old_comp_owner.getId(), ["Manager"]) #1
            obj.reindexObjectSecurity()
            pct = getToolByName(obj, 'portal_catalog')
            brain = pct({'portal_type': 'comprobacion', 'id': obj.id})[0]
            brain.changeOwnership(trip_owner, recursive=True)
            brain.manage_setLocalRoles(trip.getOwner().getId(), roles)
            brain.reindexObjectSecurity()
            #print(obj.listCreators(), obj.listCreators__roles__)
        except Exception as error:
            import pdb; pdb.set_trace()
    else:        
        print("Algo malo pasó")

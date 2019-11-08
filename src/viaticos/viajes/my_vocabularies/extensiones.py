# -*- coding: utf-8 -*-
from zope.component import getUtility
from zope.interface import provider
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from viaticos.viajes import _

@provider(IVocabularyFactory)
def estados_comprobacion(context):
    factory = getUtility(IVocabularyFactory, 'plone.app.vocabularies.WorkflowStates')
    vocabulary = factory(context)
    states = [x for x in vocabulary._terms if x.value in ("bosquejo", "revision", "aprobado")]
    return SimpleVocabulary(states)


@provider(IVocabularyFactory)
def estados_viaje(context):
    factory = getUtility(IVocabularyFactory, 'plone.app.vocabularies.WorkflowStates')
    vocabulary = factory(context)
    states = [x for x in vocabulary._terms if x.value in ("borrador", "pendiente", "esperando", "autorizado", "final")]
    return SimpleVocabulary(states)


@provider(IVocabularyFactory)
def coordinaciones(context):
    Coordinaciones = SimpleVocabulary(
        [SimpleTerm(value=u'administracion', title=_(u'Administración')),
         SimpleTerm(value=u'servicio_cliente', title=_(u'Atención y servicio al cliente')),
         SimpleTerm(value=u'comercial', title=_(u'Comercial')),
         SimpleTerm(value=u'finanzas', title=_(u'Finanzas')), 
         SimpleTerm(value=u'gestion_energia', title=_(u'Gestión de energía')),
         SimpleTerm(value=u'juridico', title=_(u'Jurídico')),
        ]
    )
    return Coordinaciones

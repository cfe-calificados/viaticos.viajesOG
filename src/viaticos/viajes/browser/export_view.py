# -*- coding: utf-8 -*-
from viaticos.viajes import _
from zope.interface import provider


from plone import api
from datetime import datetime
from Products.statusmessages.interfaces import IStatusMessage
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from plone.directives import form
from zope import schema
from z3c.form import button


Coordinaciones = SimpleVocabulary(
    [SimpleTerm(value=u'administracion', title=_(u'Administración')),
     SimpleTerm(value=u'servicio_cliente', title=_(u'Atención y servicio al cliente')),
     SimpleTerm(value=u'comercial', title=_(u'Comercial')),
     SimpleTerm(value=u'finanzas', title=_(u'Finanzas')), 
     SimpleTerm(value=u'gestion_energia', title=_(u'Gestión de energía')),
     SimpleTerm(value=u'juridico', title=_(u'Jurídico')),
    ]
)


class IVistaDescargas(form.Schema):
    
    fecha_salida = schema.Datetime(
        title = _(u'Fecha de salida'),
        required = True, 
    )

    fecha_regreso = schema.Datetime(
        title = _(u'Fecha de regreso'),
        required = True, 
    )

    areas = schema.Choice(
        title = _(u'Area'),
        vocabulary = Coordinaciones,
        required = False,
    )

    colaboradores = schema.List(
        title = _(u'Colaborador'),
        value_type=schema.Choice(
            title=_(u"Miembro"),
            vocabulary = u"plone.app.vocabularies.Users",
            required = False,
        ),
        required = False
    )
    

class VistaDescargas(form.SchemaForm):
    
    schema = IVistaDescargas
    ignoreContext = True

    label = u"Exportación de información"
    description = u"Genera un archivo .xls con la información de viaticos dado un rango de fechas, área y colaboradores"

    def update(self):
        print("Hola")
        # disable Plone's editable border
        self.request.set('disable_border', True)

        # call the base class version - this is very important!
        super(VistaDescargas, self).update()

    @button.buttonAndHandler(u'Descargar XLS')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        print(data)
        #import pdb; pdb.set_trace()
        return
    
    
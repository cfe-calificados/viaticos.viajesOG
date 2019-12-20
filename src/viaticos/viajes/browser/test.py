# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield import DataGridFieldFactory,BlockDataGridFieldFactory, datagridfield
from collective.z3cform.datagridfield import DictRow
from z3c.form import field
from plone.directives import form
from z3c.form.form import extends
from zope import interface
from zope import component
from zope import schema
from plone.dexterity.browser import edit
from plone.dexterity.browser.view import DefaultView
#import requests
from viaticos.viajes import _
from z3c.form import button
#static resources
from Products.CMFPlone.resources import add_resource_on_request

#datagrid
#from z3c.form import DataGridField


class ITableRowSchema(interface.Interface):
    one = schema.TextLine(title=u"One")
    two = schema.TextLine(title=u"Two")
    three = schema.TextLine(title=u"Three")


class IFormSchema(interface.Interface):
    one = schema.TextLine(title=u"One")
    #table = schema.List(title=u"Table",
        #value_type=DictRow(title=u"tablerow", schema=ITableRowSchema))

@component.adapter(IFormSchema)
class DataGridForm(form.EditForm):
    fields = field.Fields(IFormSchema)
    label=u"Demo Usage of DataGridField"
    #fields['table'].widgetFactory = DataGridFieldFactory
    

class Prueba(DefaultView):
    """ Prueba para JS """
    def __call__(self):
        # utility function to add resource to rendered page
        print("loading CSS")        
        add_resource_on_request(self.request, 'tabs_statics')
        return super(Prueba, self).__call__()
    
    def get_pieces(self):
        #countries = requests.get("http://battuta.medunes.net/api/country/all/?key=1dd922d979a3bed9b393e51f9eccf102")
        
        products = [
            {
                "name": "Gas",
                "id": "gas",
                "regimes": [
                    {
                        "name": "Fourth Tier",
                        "id": "4thGas",
                        "categories": [
                            {
                                "name": "TR4",
                                "id": "tr4gas"
                            },
                            {
                                "name": "TR4AG",
                                "id": "tr4ag"
                            },
                            {
                                "name": "TR4M2.5",
                                "id": "tr4m25gas"
                            }
                        ]
                    },
                    {
                        "name": "New",
                        "id": "newGas",
                        "categories": [
                            {
                                "name": "NEW 10",
                                "id": "new10gas"
                            },
                            {
                                "name": "NEW 11",
                                "id": "new11gas"
                            },
                            {
                                "name": "NEW M5",
                                "id": "newm5gas"
                            }
                        ]
                    },
                    {
                        "name": "Old",
                        "id": "oldGas",
                        "categories": [
                            {
                                "name": "Old 6.9",
                                "id": "old69gas"
                            }
                        ]
                    },
                    {
                        "name": "Third tier",
                        "id": "3rdGas",
                        "categories": [
                            {
                                "name": "TR3",
                                "id": "TR3gas"
                            },
                            {
                                "name": "TR3 M5",
                                "id": "tr3m5gas"
                            }
                        ]
                    }
                ]
            },
            {
                "name": "OIL",
                "id": "oil",
                "regimes": [
                    {
                        "name": "EOR",
                        "id": "eoroil",
                        "categories": [
                            {
                                "name": "EOR",
                                "id": "eoroil"
                            },
                            {
                                "name": "NPJEOR",
                                "id": "npjeoroil"
                            },
                            {
                                "name": "TR4M2.5",
                                "id": "tr4m25gas"
                            }
                        ]
                    },
                    {
                        "name": "Fourth Tier",
                        "id": "4thOil",
                        "categories": [
                            {
                                "name": "TR4",
                                "id": "tr4oil"
                            },
                            {
                                "name": "TR4 WF",
                                "id": "tr4wfoil"
                            },
                            {
                                "name": "TR4M2.5",
                                "id": "tr4m25oil"
                            }
                        ]
                    },
                    {
                        "name": "Old",
                        "id": "oldoil",
                        "categories": [
                            {
                                "name": "Old 6.9",
                                "id": "old69oil"
                            }
                        ]
                    },
                    {
                        "name": "Third tier",
                        "id": "3rdoil",
                        "categories": [
                            {
                                "name": "TR3",
                                "id": "TR3oil"
                            },
                            {
                                "name": "TR3 M5",
                                "id": "tr3m5oil"
                            },
                            {
                                "name": "TR3 WF",
                                "id": "tr3wfoil"
                            }
                        ]
                    }
                ]
            }
        ]

        return products

class ITabla(interface.Interface):
    fecha= schema.Datetime(title=_(u"Fecha"), required=True)
    concepto = schema.TextLine(title=_(u"Concepto"),required=True)
    


class IGridForm(form.Schema):
    """ Define form fields """

    #import pdb; pdb.set_trace()
    
    hotel_domicilio =  schema.TextLine(
        title = _(u'Domicilio del hotel'),
        required = True,
    )

    
    grupo_comprobacion = schema.List(
        title=_(u'Grupo'),
        description=_(u'Prueba de datagrid'),        
        value_type=DictRow(
            title=_(u"tablita"),
            schema=ITabla
        ),
        #default = [],
        required=True
    )

    
#@component.adapter(IGridForm)
class PruebaForm2(form.SchemaForm):
    """ Define Form handling

    This form can be accessed as http://yoursite/@@ticket-form

    """

    schema = IGridForm
    ignoreContext = True

    label = u"Lalalala"
    description = u"Probando 1... 2... 3 "

    fields = field.Fields(IGridForm)
    fields['grupo_comprobacion'].widgetFactory = DataGridFieldFactory
    #fields = field.fields(form.SchemaForm)
    
    #form.widget(grupo_comprobacion=DataGridFieldFactory)    
    @button.buttonAndHandler(u'Aceptar')
    def handleApply(self, action):
        return
    
    @button.buttonAndHandler(u"Cancelar")
    def handleCancel(self, action):
        return 


from z3c.form.interfaces import IWidgets

class ITabla2(interface.Interface):
    fecha= schema.Datetime(title=_(u"Fecha"), required=False)
    concepto = schema.TextLine(title=_(u"Concepto"),required=False)


class TablaAddForm(form.EditForm):
    #template = ViewPageTemplateFile('simple_owneredit.pt', templatePath)
     fields = field.Fields(ITabla2)
     #prefix = 'owner'

     def updateWidgets(self):
         self.widgets = component.getMultiAdapter(
             (self, self.request, self.getContent()), IWidgets)
         self.widgets.ignoreContext = True
         self.widgets.update()
         
class IGridForm2(interface.Interface):
    """ Define form fields """

    #import pdb; pdb.set_trace()
    
    hotel_domicilio =  schema.TextLine(
        title = _(u'Domicilio del hotel'),
        required = True,
    )

    
    grupo_comprobacion = schema.List(
        title = _(u"Heh"),
        min_length = 1,
        value_type = schema.Object(
            title=_(u'Grupo'),
            #description=_(u'Prueba de datagrid'),        
            schema=ITabla2,
            required=False,
        ),
    )


class PruebaForm(form.EditForm):
    fields = field.Fields(IGridForm2).select('hotel_domicilio', 'grupo_comprobacion')
     #template = ViewPageTemplateFile( 'simple_caredit.pt', templatePath)
     #prefix = 'car'
     
    def updateWidgets(self):
        self.widgets = component.getMultiAdapter(
            (self, self.request, self.getContent()), IWidgets)
        self.widgets.ignoreContext = True
        self.widgets.update()

    def update(self):
        self.grupo_comprobacion = TablaAddForm(None, self.request)
        self.grupo_comprobacion.update()
        super(PruebaForm, self).update()
    
    @button.buttonAndHandler(u'save')
    def handleApply(self, action):
        data, errors = self.extractData()
        import pdb; pdb.set_trace()

    @button.buttonAndHandler(u'cancel')
    def handleApply(self, action):
        data, errors = self.extractData()
        import pdb; pdb.set_trace()


class PruebaForm3(form.SchemaForm):
    """ Define Form handling

    This form can be accessed as http://yoursite/@@ticket-form

    """
    schema = IGridForm2
    ignoreContext = True

    label = u"Lalalala"
    description = u"Probando 1 2 3 "
    fields = field.Fields(IGridForm2)



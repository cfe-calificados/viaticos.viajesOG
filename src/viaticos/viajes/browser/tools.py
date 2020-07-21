# -*- coding: utf-8 -*-
from plone.directives import form
from zope import schema
from z3c.form import button
from plone.namedfile.field import NamedBlobFile
from viaticos.viajes import _
from Products.CMFCore.utils import getToolByName
import csv

class IUserCSV(form.Schema):
    archivo = NamedBlobFile(
        title=_(u'Archivo'),
        description=u"CSV de usuarios.",
        required = True
    )

class UserCSVForm(form.SchemaForm):
    schema = IUserCSV
    label = u"Registro de usuarios"
    ignoreContext = True

    def register_users(self, data):
        #import pdb; pdb.set_trace()
        if data['archivo'] == None or data['archivo'].contentType != "text/csv":
            return False, "Archivo vacío o formato incorrecto."

        regtool = getToolByName(self.context, 'portal_registration')
        ceseve = csv.reader(data['archivo'].data.split("\n"), delimiter=',', quotechar='"')
        for line in ceseve:            
            if not line: continue
            line = [x.strip() for x in line]
            print line
            try:
                properties = dict(username = line[0],fullname = line[0], email = line[1],)
                member = regtool.addMember(line[0], line[2], properties=properties)
                print("Usuario registrado exitosamente: "+line[0])
            except Exception as error:
                print(error)
                return False, "Problema con el usuario: "+line[0]
                
                    
        return True,"Éxito"
    
    @button.buttonAndHandler(u"Aceptar")
    def handleApply(self, action):
	data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            #import pdb; pdb.set_trace()
            return
        success,message = self.register_users(data)
        self.status = message
        return

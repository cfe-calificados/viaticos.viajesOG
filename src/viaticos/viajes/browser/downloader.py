# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone import api
from plone.namedfile.file import NamedBlobFile as BlobFile
from plone.namedfile.utils import set_headers
from plone.namedfile.utils import stream_data
from Products.CMFCore.utils import getToolByName


class ComprobacionesDownloader(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request


    def __call__(self):
        return self.downloadFile()
    

    def get_row(self, comprobacion):
        """
        comprobacion: transformación de un objeto de comprobación a cadena para csv.
        POR TERMINAR
        """
        return  comprobacion.Title().decode('utf-8')


    def query_catalog(self, search_params):
        """
        search_params: diccionario que contiene los parámetros de búsqueda para el portal_catalog
        POR TERMINAR
        """
        comprobaciones = []
        try:
            pctl = self.context.portal_catalog
        except Exception as error:
            print(error)
            pctl = getToolByName(context, 'portal_catalog')
        brains = pctl(portal_type='comprobacion', Creator=search_params['user'])
        #filter brains by date        
        for brain in brains:
            obj = brain.getObject()
            if True: #filter by date and owner area
                comprobaciones.append(obj)
        return comprobaciones
    

    def downloadFile(self):
        """
        Función para descarga de csv con encoding de windows
        """
        params = {'user': None, 'date_ini': None, 'date_fin': None, 'coordinacion': None}
        url_form = self.request.form
        if url_form:
            print(url_form)
            if url_form.has_key('user'): params['user'] = url_form['user']
            if url_form.has_key('date_ini'): params['date_ini'] = url_form['date_ini']
            if url_form.has_key('date_fin'): params['date_fin'] = url_form['date_fin']
            if url_form.has_key('coordinacion'): params['coordinacion'] = url_form['coordinacion']
            
        comps_list = self.query_catalog(params)
        
        header = u"Colaborador,Coordinación,Lugar,Fecha de salida, Fecha de regreso,Monto Avión,Monto Hotel,Monto Alimentos,Monto Otros,Fecha de Comprobación,Monto Aprobado,Fecha Autorización Finanzas,\n"
        
        body = u""
        for comprobacion in map(self.get_row, comps_list):
            body += comprobacion + u"\n"
            
        file_text = header.encode('cp1252') + body.encode('cp1252')
        blob = BlobFile(bytes(file_text), filename=('ReporteComprobaciones.csv').decode('utf-8'))
        if blob is None:
	    raise NotFound('No file present')
        
	filename = getattr(blob, 'filename', self.context.id + '_download')        
	set_headers(blob, self.request.response)

        self.request.response.setHeader('Content-Type', 'text/csv')
	self.request.response.setHeader('Content-Disposition', 'attachment; filename="%s"' % filename)

        #self.request.response.setBody('', lock=True)
        
	return stream_data(blob)

        
        

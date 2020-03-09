from Products.Five.browser import BrowserView
from plone import api
from DateTime import DateTime
from datetime import datetime, timedelta

class TestChronos(BrowserView):
    def __call__(self):
        #import pdb; pdb.set_trace()
        if not self.request.form:
            authenticator = self.context.restrictedTraverse("@@authenticator")
            self.request.form['_authenticator'] = authenticator.token()            
        if self.request.form:
            #import pdb; pdb.set_trace()
            print("Chronos is hungry...")
            pctl = api.portal.get_tool('portal_catalog')
            pwfl = api.portal.get_tool('portal_workflow')
            all_trips = pctl({'portal_type':'viaje', 'review_state':'revision aprobador'})
            for trip in all_trips:
                if (DateTime().asdatetime()-trip.modified.asdatetime()).total_seconds()/60 > 2:
                    pwfl.doActionFor(trip.getObject(), 'aprobar_solicitud')
            return "Chronos eats his own children"

        #authenticator = self.context.restrictedTraverse("@@authenticator")
        #self.request.response.redirect(self.context.absolute_url()+"/make-transitions?_authenticator=" + authenticator.token())
        #import pdb; pdb.set_trace()
        
                

# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import viaticos.viajes


class ViaticosViajesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=viaticos.viajes)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'viaticos.viajes:default')


VIATICOS_VIAJES_FIXTURE = ViaticosViajesLayer()


VIATICOS_VIAJES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VIATICOS_VIAJES_FIXTURE,),
    name='ViaticosViajesLayer:IntegrationTesting',
)


VIATICOS_VIAJES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VIATICOS_VIAJES_FIXTURE,),
    name='ViaticosViajesLayer:FunctionalTesting',
)


VIATICOS_VIAJES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        VIATICOS_VIAJES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='ViaticosViajesLayer:AcceptanceTesting',
)

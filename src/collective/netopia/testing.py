# -*- coding: utf-8 -*-
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE,
    PloneSandboxLayer,
)
from plone.testing import z2

import collective.netopia


class CollectiveNetopiaLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.netopia)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.netopia:default")


COLLECTIVE_NETOPIA_FIXTURE = CollectiveNetopiaLayer()


COLLECTIVE_NETOPIA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_NETOPIA_FIXTURE,),
    name="CollectiveNetopiaLayer:IntegrationTesting",
)


COLLECTIVE_NETOPIA_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_NETOPIA_FIXTURE,),
    name="CollectiveNetopiaLayer:FunctionalTesting",
)


COLLECTIVE_NETOPIA_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_NETOPIA_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectiveNetopiaLayer:AcceptanceTesting",
)

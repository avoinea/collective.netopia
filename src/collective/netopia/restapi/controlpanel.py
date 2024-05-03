""" Controlpanel API
"""
from zope.interface import Interface
from zope.component import adapter
from plone.restapi.controlpanels import RegistryConfigletPanel
from collective.netopia.interfaces import ICollectiveNetopiaSettings
from collective.netopia.interfaces import ICollectiveNetopiaLayer


@adapter(Interface, ICollectiveNetopiaLayer)
class Controlpanel(RegistryConfigletPanel):
    """ Control Panel"""

    schema = ICollectiveNetopiaSettings
    configlet_id = "netopia"
    configlet_category_id = "Products"
    schema_prefix = None

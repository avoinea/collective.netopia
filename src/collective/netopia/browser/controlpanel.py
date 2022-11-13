""" Control Panel
"""
from plone.app.registry.browser import controlpanel
from collective.netopia.interfaces import ICollectiveNetopiaSettings
from collective.netopia import _


class ControlPanelForm(controlpanel.RegistryEditForm):
    """ControlPanelForm."""

    id = "netopia"
    label = _("Netopia Payments")
    schema = ICollectiveNetopiaSettings


class ControlPanelView(controlpanel.ControlPanelFormWrapper):
    """Control Panel"""

    form = ControlPanelForm

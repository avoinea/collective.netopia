# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from zope.interface import Interface
from zope import schema
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from collective.netopia import _


class ICollectiveNetopiaLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICollectiveNetopiaSignedOrder(Interface):
    """Netopia Signed Order Utility"""


class ICollectiveNetopiaSettings(Interface):
    """Netopia Payments MobilPay settings"""

    server = schema.TextLine(
        title=_("API URL"),
        description=_("Netopia Payments MobilPay API URL"),
        default="https://sandboxsecure.mobilpay.ro",
    )

    signature = schema.TextLine(
        title=_("Signature"),
        description=_(
            "Netopia Payments MobilPay unique key that identifies your point of sale in the payment process."
        ),
        default="",
    )

    private = schema.Text(
        title=_("Private KEY"),
        description=("Netopia Payments MobilPay Private KEY"),
        default="",
    )

    public = schema.Text(
        title=_("Public KEY"),
        description=("Netopia Payments MobilPay Public KEY"),
        default="",
    )


class ICollectiveNetopiaOrder(Interface):
    """ Marker interface for Collective Netopia Order """

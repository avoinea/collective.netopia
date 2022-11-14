# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from zope.interface import Interface
from zope.interface.interfaces import IObjectEvent
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

    return_url = schema.TextLine(
        title=_("Return URL"),
        description=_(
            "The redirect URL will be used to redirect User/Customer "
            "back to the Merchant's website from NETOPIA Payments "
            "(from the payment page, after the payment is done). "
            "Leave empty to redirect to the Order URL. "
            "You can redirect to order URL + dedicated view: e.g. thank-you. "
            "Start with / to redirect to Site Root relative path: e.g.: /user-account. "
            "You can also provide an absolute_url "
            "like: https://www.example.com/thank-you"
        ),
        default="",
        required=False,
    )

    confirm_url = schema.TextLine(
        title=_("Confirm URL"),
        description=_(
            "The confirm URL will be used for IPN (Instant Payment Notification) - "
            "i.e. to send information about the transaction's status. "
            "If you're not sure about this use default value: netopia.confirm. "
            "You can implement your custom confirmation order URL: "
            "e.g. custom-confirmation. "
            "Start with / to use a Site Root relative path: "
            "e.g.: /global-confirmation. "
            "You can also provide an absolute_url like: "
            "https://www.example.com/global-confirmation-webhook"
        ),
        default="netopia.confirm",
    )

    signature = schema.TextLine(
        title=_("Signature"),
        description=_(
            "Netopia Payments MobilPay unique key that identifies "
            "your point of sale in the payment process."
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
    """Marker interface for Collective Netopia Order"""


#
# Events
#
class ICollectiveNetopiaEvent(IObjectEvent):
    """Custom Event"""


class IPaymentEvent(ICollectiveNetopiaEvent):
    """All payment events should inherit from this"""


class IPaymentConfirmedEvent(IPaymentEvent):
    """Payment status: confirmed"""


class IPaymentConfirmedPendingEvent(IPaymentEvent):
    """Payment status: confirmed_pending"""


class IPaymentPaidPendingEvent(IPaymentEvent):
    """Payment status: paid_pending"""


class IPaymentPaidEvent(IPaymentEvent):
    """Payment status: paid"""


class IPaymentCancelledEvent(IPaymentEvent):
    """Payment status: cancelled"""


class IPaymentCreditEvent(IPaymentEvent):
    """Payment status: credit"""


class IPaymentRejectedEvent(IPaymentEvent):
    """Payment status: rejected"""

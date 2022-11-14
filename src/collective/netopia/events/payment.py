""" Custom payment events
"""
from zope.interface import implementer
from collective.netopia.interfaces import IPaymentEvent
from collective.netopia.interfaces import IPaymentConfirmedEvent
from collective.netopia.interfaces import IPaymentConfirmedPendingEvent
from collective.netopia.interfaces import IPaymentPaidPendingEvent
from collective.netopia.interfaces import IPaymentPaidEvent
from collective.netopia.interfaces import IPaymentCancelledEvent
from collective.netopia.interfaces import IPaymentCreditEvent
from collective.netopia.interfaces import IPaymentRejectedEvent


@implementer(IPaymentEvent)
class PaymentEvent:
    """Custom payment event"""

    def __init__(self, context, **kwargs):
        self.object = context
        for key, value in kwargs.items():
            setattr(self, key, value)


@implementer(IPaymentConfirmedEvent)
class PaymentConfirmedEvent(PaymentEvent):
    """Payment status: confirmed"""


@implementer(IPaymentConfirmedPendingEvent)
class PaymentConfirmedPendingEvent(PaymentEvent):
    """Payment status: confirmed_pending"""


@implementer(IPaymentPaidPendingEvent)
class PaymentPaidPendingEvent(PaymentEvent):
    """Payment status: paid_pending"""


@implementer(IPaymentPaidEvent)
class PaymentPaidEvent(PaymentEvent):
    """Payment status: paid"""


@implementer(IPaymentCancelledEvent)
class PaymentCancelledEvent(PaymentEvent):
    """Payment status: cancelled"""


@implementer(IPaymentCreditEvent)
class PaymentCreditEvent(PaymentEvent):
    """Payment status: credit"""


@implementer(IPaymentRejectedEvent)
class PaymentRejectedEvent(PaymentEvent):
    """Payment status: rejected"""

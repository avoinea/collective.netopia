""" Netopia Payments MobilPay Signed Order

Minimum required DX context attributes:

    >>> context.__dict__
    ... {
                "return_url": "https://www.avoinea.com/order/1",
                "confirm_url": "https://www.avoinea.com/order/1/confirm",
                "currency": "RON",
                "price": "0.10",
                "details": "Test payment",
                "billing": "person",
                "first_name": "Alin",
                "last_name": "Voinea",
                "address": "Bucharest, Romania",
                "email": "collective.netopia@mailinator.com",
                "phone": "0123456789",
    ... }

Optionally you can provide different shipping details:

    >>> context.__dict__
    ... {
                "shipping": "person",
                "shipping_first_name": "George",
                "shipping_last_name": "Voinea",
                "shipping_address": "Arges, Romania",
                "shipping_email": "collective.netopia@mailinator.com",
                "shipping_phone": "987654321",
    ... }

By default the order "id" and "token" are the same with context UUID.
You can override them like:

    >>> context.__dict__
    ... {
                "order_id": "custom-order-id",
                "token": "custom-token-id"
    ... }

    >>> from zope.component import getMultiAdapter
    >>> signed_order = getMultiAdapter((self.context, self.request), name="netopia")
    >>> data = signed_order()

Send a POST request with your signed order:

    >>> import requests
    >>> r = requests.post(signed_order.server(), data=data)

Get status code

    >>> r.status_code
    STATUS_CODE

    >>> r.reason
    REASON

Response

    >>> r.text


"""
import logging
from urllib.parse import unquote
from zope.event import notify
from zope.component import queryUtility
from plone.uuid.interfaces import IUUID
from plone import api
from plone.restapi.deserializer import json_body
from collective.netopia.mobilpay.request import Request
from collective.netopia.mobilpay.payment.request.crc import Crc
from collective.netopia.interfaces import ICollectiveNetopiaSignedOrder
from collective.netopia.interfaces import ICollectiveNetopiaSettings
from collective.netopia.events.payment import PaymentSignedEvent
from collective.netopia.events.payment import PaymentConfirmedEvent
from collective.netopia.events.payment import PaymentConfirmedPendingEvent
from collective.netopia.events.payment import PaymentPaidPendingEvent
from collective.netopia.events.payment import PaymentPaidEvent
from collective.netopia.events.payment import PaymentCancelledEvent
from collective.netopia.events.payment import PaymentCreditEvent
from collective.netopia.events.payment import PaymentRejectedEvent

from Products.Five.browser import BrowserView

logger = logging.getLogger("collective.netopia")


class NetopiaSignedOrder(BrowserView):
    """Netopia Payments Signed Order"""

    def __init__(self, context, request):
        super(NetopiaSignedOrder, self).__init__(context, request)

        # Server settings
        self._server = None
        self._signature = None
        self._public_key = None
        self._return_url = None
        self._confirm_url = None

        # Order details.
        self._order = None

        # Signed order
        self._signed_order = None

    #
    # Server settings
    #
    def server(self):
        """Server URL"""
        if self._server is None:
            self._server = api.portal.get_registry_record(
                "server", interface=ICollectiveNetopiaSettings, default=""
            )
        return self._server

    @property
    def signature(self):
        """Signature"""
        if self._signature is None:
            self._signature = api.portal.get_registry_record(
                "signature", interface=ICollectiveNetopiaSettings, default=""
            )
        return self._signature

    @property
    def public_key(self):
        """Public Key"""
        if self._public_key is None:
            self._public_key = api.portal.get_registry_record(
                "public", interface=ICollectiveNetopiaSettings, default=""
            )
        return self._public_key

    @property
    def return_url(self):
        """Return URL"""
        if self._return_url is None:
            self._return_url = (
                api.portal.get_registry_record(
                    "return_url", interface=ICollectiveNetopiaSettings, default=""
                )
                or ""
            )
            # Site relative path
            if self._return_url.startswith("/"):
                self._return_url = api.portal.get().absolute_url() + self._return_url
            # Context relative path
            if not self._return_url.startswith("http"):
                self._return_url = "/".join(
                    (self.context.absolute_url(), self._return_url)
                )
            logger.warning("return_url: %s", self._return_url)
        return self._return_url

    @property
    def confirm_url(self):
        """Confirm URL"""
        if self._confirm_url is None:
            self._confirm_url = (
                api.portal.get_registry_record(
                    "confirm_url", interface=ICollectiveNetopiaSettings, default=""
                )
                or ""
            )
            # Site relative path
            if self._confirm_url.startswith("/"):
                self._confirm_url = api.portal.get().absolute_url() + self._confirm_url
            # Context relative path
            if not self._confirm_url.startswith("http"):
                self._confirm_url = "/".join(
                    (self.context.absolute_url(), self._confirm_url)
                )
            logger.warning("confirm_url: %s", self._confirm_url)
        return self._confirm_url

    @property
    def order(self):
        """Order details"""
        if self._order is None:
            self._order = {
                "signature": self.signature,
                "public_key": self.public_key,
                "amount": self.context.price,
                "details": self.context.Description() or self.context.Title(),
                "first_name": self.context.first_name,
                "last_name": self.context.last_name,
                "address": self.context.address,
                "email": self.context.email,
                "phone": self.context.phone,
                "confirm_url": self.confirm_url,
                "return_url": self.return_url,
                "id": getattr(self.context, "order_id", None) or IUUID(self.context),
                "token": getattr(self.context, "token", None) or IUUID(self.context),
                "currency": getattr(self.context, "currency", None) or "RON",
                "billing": getattr(self.context, "billing", None) or "person",
                "shipping": getattr(self.context, "shipping", None)
                or getattr(self.context, "billing", "person"),
                "shipping_first_name": getattr(
                    self.context, "shipping_first_name", None
                )
                or self.context.first_name,
                "shipping_last_name": getattr(self.context, "shipping_last_name", None)
                or self.context.last_name,
                "shipping_address": getattr(self.context, "shipping_address", None)
                or self.context.address,
                "shipping_email": getattr(self.context, "shipping_email", None)
                or self.context.email,
                "shipping_phone": getattr(self.context, "shipping_phone", None)
                or self.context.phone,
            }
        return self._order

    @property
    def signed_order(self):
        """Return signed order with public_key"""
        if self._signed_order is None:
            sign = queryUtility(ICollectiveNetopiaSignedOrder)
            self._signed_order = sign(**self.order)
            notify(
                PaymentSignedEvent(
                    self.context, status="signed", code=0, msg="Payment signed"
                )
            )
        return self._signed_order


class NetopiaPay(NetopiaSignedOrder):
    """Pay Signed Order"""


class NetopiaConfirm(BrowserView):
    """Confirm payment"""

    def __init__(self, context, request):
        super(NetopiaConfirm, self).__init__(context, request)
        self._private_key = None

    @property
    def private_key(self):
        """Private Key"""
        if self._private_key is None:
            self._private_key = api.portal.get_registry_record(
                "private", interface=ICollectiveNetopiaSettings, default=""
            )
        return self._private_key

    def confirmed(self, code, msg):
        """
        When the action is confirmed, we are certain that the
        money has left the card holder's account and we update the
        status of the order and the delivery of the product
        """
        # update DB, SET status = "confirmed/captured"
        notify(
            PaymentConfirmedEvent(self.context, status="confirmed", code=code, msg=msg)
        )

    def confirmed_pending(self, code, msg):
        """
        When the action is confirmed_pending, it means that the
        transaction is being checked against fraud. We do not do
        delivery/shipping. After passing this check, you will receive
        a new notification for a confirmation or cancellation action.
        """
        # update DB, SET status = "pending"
        notify(
            PaymentConfirmedPendingEvent(
                self.context, status="pending", code=code, msg=msg
            )
        )

    def paid_pending(self, code, msg):
        """
        When the action is paid_pending, it means that the transaction
        is being verified. We do not do delivery/shipping.
        After passing this check, you will receive a new notification
        for a confirmation or cancellation action.
        """
        # update DB, SET status = "paid_pending"
        notify(
            PaymentPaidPendingEvent(
                self.context, status="paid_pending", code=code, msg=msg
            )
        )

    def paid(self, code, msg):
        """
        When the action is paid, it means that the transaction is being
        processed. We do not do delivery/shipping.
        After going through this processing, a new notification will be
        received for a confirmation or cancellation action.
        """
        # update DB, SET status = 'open/preauthorized'
        notify(PaymentPaidEvent(self.context, status="open", code=code, msg=msg))

    def canceled(self, code, msg):
        """
        When the action is canceled, it means that the transaction
        is cancelled. We do not do delivery/shipping.
        """
        # update DB, SET status = 'canceled'
        notify(
            PaymentCancelledEvent(self.context, status="canceled", code=code, msg=msg)
        )

    def credit(self, code, msg):
        """
        When the action is credit, it means that the money is returned
        to the card holder. If a delivery has already been made,
        it must be stopped or reversed.
        """
        # update DB, SET status = 'refunded'
        notify(PaymentCreditEvent(self.context, status="refunded", code=code, msg=msg))

    def rejected(self, code, msg):
        """
        When the action is rejected, it means that the transaction
        is rejected. We do not do delivery/shipping.
        """
        notify(
            PaymentRejectedEvent(self.context, status="refunded", code=code, msg=msg)
        )
        # update DB, SET status = 'rejected'

    def xml(self, error_code, error_type, error_message):
        """Return Netopia Payment XML"""
        logger.warning(
            "%s: code: %s, type: %s, msg: %s",
            self.context.absolute_url(),
            error_code,
            error_type,
            error_message,
        )
        self.request.response.setHeader('Content-Type', 'application/xml; charset=utf-8')
        crc = Crc(error_code, error_type, error_message).create_crc()
        return crc.toprettyxml(indent="\t", encoding="utf-8")

    def __call__(self):
        # Invalid method
        if self.request.method.lower() != "post":
            return self.xml(
                Request.ERROR_CONFIRM_INVALID_POST_METHOD,
                Request.CONFIRM_ERROR_TYPE_PERMANENT,
                "invalid request method for payment confirmation",
            )

        form = self.request.form
        if "env_key" not in form:
            form = json_body(self.request)

        env_key = form.get("env_key")
        env_data = form.get("data")

        if (
            env_key is None
            or len(env_key) == 0
            or env_data is None
            or len(env_data) == 0
        ):
            return self.xml(
                Request.ERROR_CONFIRM_INVALID_POST_PARAMETERS,
                Request.CONFIRM_ERROR_TYPE_PERMANENT,
                "mobilpay.ro posted invalid parameters",
            )

        error_code = 0
        error_type = Request.CONFIRM_ERROR_TYPE_NONE
        error_message = ""

        # if env_key == 'TEST' and env_data == 'TEST':
            # self.confirmed(error_code, "TEST")
            # return self.xml(1, 36, 'fraud')

        try:
            req = Request().factory_from_encrypted(
                unquote(env_key), unquote(env_data), self.private_key
            )
            req_notify = req.get_notify()
            if int(req_notify.errorCode) == 0:
                if req_notify.action == "confirmed":
                    self.confirmed(req_notify.errorCode, req_notify.errorMessage)
                    error_message = req_notify.errorMessage
                elif req_notify.action == "confirmed_pending":
                    self.confirmed_pending(
                        req_notify.errorCode, req_notify.errorMessage
                    )
                    error_message = req_notify.errorMessage
                elif req_notify.action == "paid_pending":
                    self.paid_pending(req_notify.errorCode, req_notify.errorMessage)
                    error_message = req_notify.errorMessage
                elif req_notify.action == "paid":
                    self.paid(req_notify.errorCode, req_notify.errorMessage)
                    error_message = req_notify.errorMessage
                elif req_notify.action == "canceled":
                    self.canceled(req_notify.errorCode, req_notify.errorMessage)
                    error_message = req_notify.errorMessage
                elif req_notify.action == "credit":
                    self.credit(req_notify.errorCode, req_notify.errorMessage)
                    error_message = req_notify.errorMessage
                else:
                    self.rejected(req_notify.errorCode, req_notify.errorMessage)
                    error_type = Request.CONFIRM_ERROR_TYPE_PERMANENT
                    error_code = Request.ERROR_CONFIRM_INVALID_ACTION
                    error_message = "mobilpay_reference_action parameters is invalid"
            else:
                error_message = req_notify.errorMessage
                error_type = Request.CONFIRM_ERROR_TYPE_TEMPORARY
                error_code = req_notify.errorCode
                self.rejected(error_code, error_message)
        except Exception as err:
            error_type = Request.CONFIRM_ERROR_TYPE_TEMPORARY
            error_message, error_code = err.args[0], err.args[1]
            self.rejected(error_code, error_message)

        return self.xml(error_code, error_type, error_message)

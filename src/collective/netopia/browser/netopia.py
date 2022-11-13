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
from zope.component import queryUtility
from plone.uuid.interfaces import IUUID
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.netopia.interfaces import ICollectiveNetopiaSignedOrder
from collective.netopia.interfaces import ICollectiveNetopiaSettings

from plone import api
from Products.Five.browser import BrowserView


class NetopiaSignedOrder(BrowserView):
    """Netopia Payments Signed Order"""

    def __init__(self, context, request):
        super(NetopiaSignedOrder, self).__init__(context, request)

        # Server settings
        self._server = None
        self._signature = None
        self._public = None

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
    def public(self):
        """Public Key"""
        if self._public is None:
            self._public = api.portal.get_registry_record(
                "public", interface=ICollectiveNetopiaSettings, default=""
            )
        return self._public

    @property
    def order(self):
        """Order details"""
        if self._order is None:
            self._order = {
                "signature": self.signature,
                "public_key": self.public,
                "amount": self.context.price,
                "details": self.context.Description() or self.context.Title(),
                "first_name": self.context.first_name,
                "last_name": self.context.last_name,
                "address": self.context.address,
                "email": self.context.email,
                "phone": self.context.phone,
                "confirm_url": getattr(self.context, "confirm_url", None) or
                               self.context.absolute_url() + '/netopia.confirm',
                "return_url": getattr(self.context, "return_url", None) or
                              self.context.absolute_url(),
                "id": getattr(self.context, "order_id", IUUID(self.context)),
                "token": getattr(self.context, "token", IUUID(self.context)),
                "currency": getattr(self.context, "currency", "RON"),
                "billing": getattr(self.context, "billing", "person"),
                "shipping": getattr(self.context, "shipping", None) or
                            getattr(self.context, "billing", "person"),
                "shipping_first_name": getattr(self.context, "shipping_first_name", None) or
                                       self.context.first_name,
                "shipping_last_name": getattr(self.context, "shipping_last_name", None) or
                                      self.context.last_name,
                "shipping_address": getattr(self.context, "shipping_address", None) or
                                    self.context.address,
                "shipping_email": getattr(self.context, "shipping_email", None) or
                                  self.context.email,
                "shipping_phone": getattr(self.context, "shipping_phone", None) or
                                  self.context.phone,
            }
        return self._order

    @property
    def signed_order(self):
        if self._signed_order is None:
            sign = queryUtility(ICollectiveNetopiaSignedOrder)
            self._signed_order = sign(**self.order)
        return self._signed_order


class NetopiaPay(NetopiaSignedOrder):
    """ Pay Signed Order
    """


class NetopiaConfirm(BrowserView):
    """ Confirm payment
    """

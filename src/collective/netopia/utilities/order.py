""" Netopia Payments MobilPay Order Utility

Minimum required order details:

    >>> details = {
    ...   "signature": "NETOPIA_SIGNATURE",
    ...   "public_key": "NETOPIA_PUBLIC_KEY",
    ...   "return_url": "https://www.avoinea.com/order/1",
    ...   "confirm_url": "https://www.avoinea.com/order/1/confirm",
    ...   "id": "custom-order-id",
    ...   "token": "custom-token-id",
    ...   "currency": "RON",
    ...   "amount": "0.10",
    ...   "details": "Test payment",
    ...   "billing": "person",
    ...   "first_name": "Alin",
    ...   "last_name": "Voinea",
    ...   "address": "Bucharest, Romania",
    ...   "email": "collective.netopia@mailinator.com",
    ...   "phone": "0123456789",
    ... }

Optionally you can provide different shipping details:

    >>> details.update({
    ...   "shipping": "person",
    ...   "shipping_first_name": "George",
    ...   "shipping_last_name": "Voinea",
    ...   "shipping_address": "Arges, Romania",
    ...   "shipping_email": "collective.netopia@mailinator.com",
    ...   "shipping_phone": "987654321",
    ... })

    >>> from zope.component import getUtility
    >>> from collective.netopia.interfaces import ICollectiveNetopiaSignedOrder
    >>> order = getUtility(ICollectiveNetopiaSignedOrder)
    >>> data = order(**details)

Now you have a signed order ready to be sent to netopia payments:

    >>> data.get('env_key')
    "ENV_KEY"

    >>> data.get('data')
    "DATA"

Send a POST request with your signed order:

    >>> import requests
    >>> requests.post("https://sandboxsecure.mobilpay.ro", data=data)

"""
from collective.netopia.mobilpay.address import Address
from collective.netopia.mobilpay.invoice import Invoice
from collective.netopia.mobilpay.payment.request.card import Card


class SignedOrder:
    """Netopia Signed Order Utility"""

    def billing(self, order):
        """Billing address"""
        billing = Address("billing")
        billing.set_type(order["billing"])
        billing.set_first_name(order["first_name"])
        billing.set_last_name(order["last_name"])
        billing.set_address(order["address"])
        billing.set_email(order["email"])
        billing.set_mobile_phone(order["phone"])
        return billing

    def shipping(self, order):
        """Shipping address"""
        shipping = Address("shipping")
        shipping.set_type(order.get("shipping", order["billing"]))
        shipping.set_first_name(order.get("shipping_first_name", order["first_name"]))
        shipping.set_last_name(order.get("shipping_last_name", order["last_name"]))
        shipping.set_address(order.get("shipping_address", order["address"]))
        shipping.set_email(order.get("shipping_email", order["email"]))
        shipping.set_mobile_phone(order.get("shipping_phone", order["phone"]))
        return shipping

    def invoice(self, order):
        """Invoice"""
        invoice = Invoice()
        invoice.set_currency(order["currency"])
        invoice.set_amount(order["amount"])
        invoice.set_token_id(order["token"])
        invoice.set_details(order["details"])
        invoice.set_billing_address(self.billing(order))
        invoice.set_shipping_address(self.shipping(order))
        return invoice

    def card(self, order):
        """Card"""
        card = Card()
        card.set_signature(order["signature"])
        card.set_order_id(order["id"])
        card.set_confirm_url(order["confirm_url"])
        card.set_return_url(order["return_url"])
        card.set_invoice(self.invoice(order))
        return card

    def __call__(self, **order):
        card = self.card(order)
        card.encrypt(order["public_key"])
        return {"env_key": card.get_env_key(), "data": card.get_enc_data()}

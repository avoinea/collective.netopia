# -*- coding: utf-8 -*-

from collective.netopia import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider


class IPriceMarker(Interface):
    """Price behaviour"""


@provider(IFormFieldProvider)
class IPrice(model.Schema):
    """Price schema"""

    model.fieldset(
        "price",
        label=_("Price"),
        fields=(
            "price",
            "currency",
        ),
    )

    price = schema.TextLine(
        title=_("Price"),
        description=_("Item price"),
        required=True,
    )

    currency = schema.TextLine(
        title=_("Currency"),
        description=_("Currency"),
        default="RON",
        required=True,
    )


@implementer(IPrice)
@adapter(IPriceMarker)
class Price(object):
    """Item's price"""

    def __init__(self, context):
        self.context = context

    @property
    def price(self):
        if hasattr(self.context, "price"):
            return self.context.price
        return 0

    @price.setter
    def price(self, value):
        self.context.price = value

    @property
    def currency(self):
        if hasattr(self.context, "currency"):
            return self.context.currency
        return "ron"

    @currency.setter
    def currency(self, value):
        self.context.currency = value

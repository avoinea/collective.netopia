# -*- coding: utf-8 -*-

from collective.netopia import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider


class IBillingMarker(Interface):
    """Billing behaviour"""


@provider(IFormFieldProvider)
class IBilling(model.Schema):
    """Billing schema"""

    model.fieldset(
        "billing",
        label=_("Billing"),
        fields=(
            "first_name",
            "last_name",
            "address",
            "city",
            "state",
            "email",
            "phone",
        ),
    )

    first_name = schema.TextLine(
        title=_("First Name"),
        description=_("First Name"),
        required=True,
    )

    last_name = schema.TextLine(
        title=_("Last Name"),
        description=_("Last Name"),
        required=True,
    )

    address = schema.TextLine(
        title=_("Address"),
        description=_("Address"),
        required=True,
    )

    city = schema.TextLine(
        title=_("City"),
        description=_("City"),
        required=True,
    )

    state = schema.TextLine(
        title=_("State"),
        description=_("State"),
        required=True,
    )

    email = schema.Email(
        title=_("Email"),
        description=_("Email"),
        required=True,
    )

    phone = schema.TextLine(
        title=_("Phone"),
        description=_("Phone number"),
        required=True,
    )


@implementer(IBilling)
@adapter(IBillingMarker)
class Billing(object):
    """Item's billing info"""

    def __init__(self, context):
        self.context = context

    @property
    def first_name(self):
        if hasattr(self.context, "first_name"):
            return self.context.first_name
        return ""

    @first_name.setter
    def first_name(self, value):
        self.context.first_name = value

    @property
    def last_name(self):
        if hasattr(self.context, "last_name"):
            return self.context.last_name
        return ""

    @last_name.setter
    def last_name(self, value):
        self.context.last_name = value

    @property
    def address(self):
        if hasattr(self.context, "address"):
            return self.context.address
        return ""

    @address.setter
    def address(self, value):
        self.context.address = value

    @property
    def city(self):
        if hasattr(self.context, "city"):
            return self.context.city
        return ""

    @city.setter
    def city(self, value):
        self.context.city = value

    @property
    def state(self):
        if hasattr(self.context, "state"):
            return self.context.state
        return ""

    @state.setter
    def state(self, value):
        self.context.state = value

    @property
    def email(self):
        if hasattr(self.context, "email"):
            return self.context.email
        return ""

    @email.setter
    def email(self, value):
        self.context.email = value

    @property
    def phone(self):
        if hasattr(self.context, "phone"):
            return self.context.phone
        return ""

    @phone.setter
    def phone(self, value):
        self.context.phone = value

# -*- coding: utf-8 -*-

from collective.netopia import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider


class IShippingMarker(Interface):
    """ Shipping behaviour
    """


@provider(IFormFieldProvider)
class IShipping(model.Schema):
    """ Shipping schema
    """
    model.fieldset('shipping',
        label=_('Shipping'),
        fields=(
            'shipping_first_name',
            'shipping_last_name',
            'shipping_address',
            'shipping_email',
            'shipping_phone',
        )
    )

    shipping_first_name = schema.TextLine(
        title=_('First Name'),
        description=_("Shipping First Name"),
        required=False,
    )

    shipping_last_name = schema.TextLine(
        title=_('Last Name'),
        description=_("Shipping Last Name"),
        required=False,
    )

    shipping_address = schema.TextLine(
        title=_('Address'),
        description=_("Shipping Address"),
        required=False,
    )

    shipping_email = schema.Email(
        title=_('Email'),
        description=_("Shipping Email"),
        required=False,
    )

    shipping_phone = schema.TextLine(
        title=_('Phone'),
        description=_("Shipping Phone number"),
        required=False,
    )

@implementer(IShipping)
@adapter(IShippingMarker)
class Shipping(object):
    """ Item's shipping info
    """
    def __init__(self, context):
        self.context = context

    @property
    def shipping_first_name(self):
        if hasattr(self.context, 'shipping_first_name'):
            return self.context.shipping_first_name
        return ''

    @shipping_first_name.setter
    def shipping_first_name(self, value):
        self.context.shipping_first_name = value

    @property
    def shipping_last_name(self):
        if hasattr(self.context, 'shipping_last_name'):
            return self.context.shipping_last_name
        return ''

    @shipping_last_name.setter
    def shipping_last_name(self, value):
        self.context.shipping_last_name = value

    @property
    def shipping_address(self):
        if hasattr(self.context, 'shipping_address'):
            return self.context.shipping_address
        return ''

    @shipping_address.setter
    def shipping_address(self, value):
        self.context.shipping_address = value

    @property
    def shipping_email(self):
        if hasattr(self.context, 'shipping_email'):
            return self.context.shipping_email
        return ''

    @shipping_email.setter
    def shipping_email(self, value):
        self.context.shipping_email = value

    @property
    def shipping_phone(self):
        if hasattr(self.context, 'shipping_phone'):
            return self.context.shipping_phone
        return ''

    @shipping_phone.setter
    def shipping_phone(self, value):
        self.context.shipping_phone = value

""" GET
"""
# -*- coding: utf-8 -*-
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import adapter, queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class NetopiaSign(object):
    """ Get netopia.sign
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {"netopia.sign": {
            "@id": "{}/@netopia.sign".format(self.context.absolute_url())
        }}
        if not expand:
            return result

        if IPloneSiteRoot.providedBy(self.context):
            return result

        order = queryMultiAdapter((self.context, self.request), name='netopia.sign')
        if order:
            result["netopia.sign"].update(order.signed_order)
        return result


class NetopiaSignGet(Service):
    """Get netopia.sign information"""

    def reply(self):
        """ Reply
        """
        info = NetopiaSign(self.context, self.request)
        return info(expand=True)["netopia.sign"]
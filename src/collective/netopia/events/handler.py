""" Content-rules
"""
import logging
from zope.component import queryAdapter
from zope.annotation.interfaces import IAnnotations

from persistent.dict import PersistentDict
from plone.app.contentrules.handlers import execute

logger = logging.getLogger("collective.netopia")

ANNOTATION_KEY = "collective.netopia"


def execute_payment(event):
    """Execute payment content rules"""
    execute(event.object, event)


def payment_confirmation(obj, event):
    """ Payment confirmation event """
    anno = queryAdapter(obj, IAnnotations)
    if anno is None:
        logger.warning("IAnnotations not enabled for %s", obj)
        return

    storage = anno.get(ANNOTATION_KEY)
    if not storage:
        anno[ANNOTATION_KEY] = PersistentDict()
        storage = anno[ANNOTATION_KEY]

    storage['code'] = event.code
    storage['msg'] = event.msg

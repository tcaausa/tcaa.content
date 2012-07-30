# $Id$

"""
TCAA Assets

Provides site asset management - logo and background images etc
"""

__author__ = 'Pat Smith <pat.smith@isotoma.com>'
__docformat__ = 'restructuredtext en'
__version__ = '$Revision$'[11:-2]

from five import grok
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import Interface
from plone.directives import form
from plone.memoize.instance import memoize
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage
from Products.CMFCore.utils import getToolByName

# View
from Acquisition import aq_inner

class IAssets(form.Schema, IImageScaleTraversable):
    """Describes the asset management interface"""
    logo = NamedBlobImage(
            title=u'Site Logo (122 x 75)',
            description=u"An image used for the logo site wide",
            required=False,
        )
    background = NamedBlobImage(
            title=u'Site background tile',
            description=u"A tile image that can be repeated across and down the page as a background",
            required=False,
        )

class Assets(grok.View):
    """Utility view the provides access to site assets"""

    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('assets')

    def update(self):
        pu = getToolByName(self.context, 'portal_url')
        portal = pu.getPortalObject()
        assets = portal.get('assets')
        if assets == None:
            self.logo = None
            self.background = None
            return
        scales =  getMultiAdapter((assets, self.request), name='images')
        scaled_logo = scales.scale('logo') #, width=122, height=75)
        if scaled_logo is None:
            self.logo = None
        else:
            self.logo = scaled_logo.url
        scaled_bg = scales.scale('background')
        if scaled_bg is None:
            self.background = None
        else:
            self.background = scaled_bg.url
    
    def render(self):
        return self

    

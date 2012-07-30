# $Id$

"""
TCAA Contact Page

A page that lists contact information
"""

__author__ = 'Pat Smith <pat.smith@isotoma.com>'
__docformat__ = 'restructuredtext en'
__version__ = '$Revision$'[11:-2]

from five import grok
from plone.app.textfield import RichText
from plone.directives import form
from zope import schema

from tcaa.content.basepage import IBasePage

#View
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from plone.memoize.instance import memoize
from tcaa.content.interfaces import ITCAASettings

class IContactPage(IBasePage):
    """Describes a contact page
    """

    locationOne = RichText(
            title=u"Office Location One",
            description=u" An office address",
        )
    locationTwo = RichText(
            title=u"Office Location Two",
            description=u" An office address",
        )
    locationThree = RichText(
            title=u"Office Location Three",
            description=u" An office address",
        )
    zoneOne = RichText(
            title=u"First Column of Contacts",
            description=u"Content for the first column of contacts",
        )
    zoneTwo = RichText(
            title=u"Second Column of Contacts",
            description=u"Content for the second column of contacts",
        )
    zoneThree = RichText(
            title=u"Third Column of contacts",
            description=u"Content for the third column of contacts",
        )

    # Deprecated fields:
    form.omitted('content_layout')
    form.omitted('borderColor')
    form.omitted('backgroundColor')
    form.omitted('whiteText')
    form.omitted('locationOne')
    form.omitted('locationTwo')
    form.omitted('locationThree')
    form.omitted('zoneOne')
    form.omitted('zoneTwo')
    form.omitted('zoneThree')

class Fragment(grok.View):
    """A view that returns the markup fragment for a contact page.
    Can be call directly or by another view.

    template: contact_templates/fragment.pt
    """
    grok.context(IContactPage)
    grok.require('zope2.View')
    grok.name('fragment')

    @memoize
    def socialLinks(self):
        registry = queryUtility(IRegistry)
        if registry is None:
            return []
        settings = registry.forInterface(ITCAASettings, check=False)
        social_links = []
        if settings.social_links:
            for setting in settings.social_links:
                title, url = setting.split('|')
                social_links.append({'title':title, 'url':url})
        return social_links


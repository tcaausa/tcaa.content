from cgi import escape

from five import grok
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from plone.app.layout.viewlets.interfaces import IHtmlHead
from Products.CMFPlone.utils import safe_unicode

from tcaa.content.interfaces import ITCAAContentish
from tcaa.content.controlpanel import TCAASettings


class TCAADublinCoreViewlet(grok.Viewlet):

    grok.name('tcaa.htmlhead.dublincore')
    grok.context(ITCAAContentish)
    grok.require('zope2.View')
    grok.viewletmanager(IHtmlHead)

    def update(self):
        context = aq_inner(self.context)
        self.metatags = []
        if hasattr(context, 'metaTitle'):
            self.metatags.append({'name': 'title',
                                  'content': context.metaTitle})
        if hasattr(context, 'metaDescription'):
            self.metatags.append({'name': 'description',
                                  'content': context.metaDescription})
        if hasattr(context, 'metaKeywords'):
            self.metatags.append({'name': 'keywords',
                                  'content': context.metaKeywords})


class TCAATitleViewlet(grok.Viewlet):
    grok.name('plone.htmlhead.title')
    grok.context(ITCAAContentish)
    grok.require('zope2.View')
    grok.viewletmanager(IHtmlHead)

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
        portalTitle = escape(safe_unicode(portal_state.navigation_root_title()))
        pageTitle = self._currentTitle()
        self.site_title = u"%s &mdash; %s" % (pageTitle, portalTitle)

    def _currentTitle(self):
        settings = TCAASettings()
        title = settings.forName('html_title', '')
        return title

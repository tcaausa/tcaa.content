

from five import grok
from Acquisition import aq_inner

from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.interfaces import IHtmlHead

from tcaa.content.interfaces import ITCAAContentish

class TCAADublinCoreViewlet(grok.Viewlet):

    grok.name('tcaa.htmlhead.dublincore')
    grok.context(ITCAAContentish)
    grok.require('zope2.View')
    grok.viewletmanager(IHtmlHead)

    def update(self):
        context = aq_inner(self.context)
        self.metatags = []
        if hasattr(context, 'metaTitle'):
            self.metatags.append({'name':'title','content':context.metaTitle})
        if hasattr(context, 'metaDescription'):
            self.metatags.append({'name':'description','content':context.metaDescription})
        if hasattr(context, 'metaKeywords'):
            self.metatags.append({'name':'keywords','content':context.metaKeywords})


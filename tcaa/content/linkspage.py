# $Id$

"""
TCAA Links Page

A page that uses naviationImages to link to other pages on the site
"""

__author__ = 'Pat Smith <pat.smith@isotoma.com>'
__docformat__ = 'restructuredtext en'
__version__ = '$Revision$'[11:-2]


from five import grok
from plone.directives import form
from plone.formwidget.contenttree import ObjPathSourceBinder
from zope import schema
from z3c.relationfield.schema import RelationList, RelationChoice

from tcaa.content.basepage import IBasePage 

# View
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter


class ILinksPage(IBasePage):
    """Describes a links page

    """
    featuredPages = RelationList(
            title=u"Featured Links",
            description=u"Six other pages to be listed on this page",
            value_type=RelationChoice(
                source=ObjPathSourceBinder(
                    object_provides=IBasePage.__identifier__
                ),
            )
        )

    form.omitted('content')
    form.omitted('content_layout')
    form.omitted('borderColor')
    form.omitted('backgroundColor')


class Fragment(grok.View):
    """A view that returns the markup fragment for a links page that
    can be called directly or by another view.

    template: linkspage_templates/fragment.pt
    """
    grok.context(ILinksPage)
    grok.require('zope2.View')
    grok.name('fragment')

    def update(self):
        """Prepare information for the template
        """
        self.hasFeaturedPages = len(self.featuredPages()) > 0

    @memoize
    def featuredPages(self):
        pages = []
        if self.context.featuredPages is not None:
            for ref in self.context.featuredPages:
                obj = ref.to_object
                scales = getMultiAdapter((obj, self.request), name='images')
                scale = scales.scale('navigationImage', width=282, height=224) 
                imageTag = None
                if scale is not None:
                    imageTag = scale.tag()
                pages.append({
                    'url': '/' + '/'.join(obj.getPhysicalPath()[2:]),
                    'title': obj.title,
                    'description': obj.description,
                    'imageTag': imageTag,
                    })
        return pages


# $Id$

"""
TCAA navigation portlet

This navigation portlet is separate and distinct from the standard plone
navigation portlet.
"""

__author__ = 'Pat Smith <pat.smith@isotoma.com>'
__docformat = 'restructuredtext en'
__version__ = '$Revision$'[11:-2]


from zope import schema
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.ATContentTypes.interfaces.link import IATLink
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from tcaa.content.interfaces import ITCAAContentish
from tcaa.content.controlpanel import TCAASettings


# Portlet configuration interface
class INavigationPortlet(IPortletDataProvider):

    count = schema.Int(
            title=u"Number of things",
            description=u"Ignore me",
            required=False,
            default=4,
        )


# Persistent class to store per instance configuation
class Assignment(base.Assignment):

    implements(INavigationPortlet)

    def __init__(self, count=4):
        self.count = count

    title = u"TCAA Navigation"


# View class
class Renderer(base.Renderer):

    # render() will be called to render the portlet
    render = ViewPageTemplateFile('navigation.pt')

    def update(self):
        self.settings = TCAASettings()

    # Always available
    def available(self):
        return True

    def tree(self):
        """
        """
        return self._data()

    @memoize
    def email(self):
        return 'mailto:%s' % self.settings.forName('email_account', '')

    @memoize
    def facebook(self):
        return 'http://www.facebook.com/%s' % self.settings.forName('facebook_account', '')

    @memoize
    def linkedin(self):
        return 'http://www.linkedin.com/%s' % self.settings.forName('linkedin_account', '')

    @memoize
    def twitter(self):
        return 'http://twitter.com/#!/%s' % self.settings.forName('twitter_account', '')

    @memoize
    def _data(self):
        pc = getToolByName(self.context, 'portal_catalog')
        pu = getToolByName(self.context, 'portal_url')
        portal = pu.getPortalObject()
        path = portal.getPhysicalPath()
        q = {'path': {'query': '/'.join(path), 'depth': 1},
             'review_state': 'published',
             'sort_on': 'getObjPositionInParent',
             'object_provides': (ITCAAContentish.__identifier__, IATLink.__identifier__,),
             }
        tree = []
        results = pc(q)
        for branch in results:
            branch_nodes = []
            pages = []

            if branch.portal_type == 'Link':
                url = branch.getRemoteUrl
                branch_nodes.append({"url": url, "title": branch.Title, "pages": pages})
            elif branch.portal_type != 'tcaa.content.Section':
                url = "/%s" % (branch.id)
                branch_nodes.append({"url": url, "title": branch.Title, "pages": pages})
            else:
                path = list(portal.getPhysicalPath())
                path.append(branch.id)
                q['path'] = {'query': '/'.join(path), 'depth': 1}
                page_brains = pc(q)
                first_page_url = None
                for page in page_brains:
                    url = "/%s/%s" % (branch.id, page.id)
                    if first_page_url == None:
                        first_page_url = url
                    if page.Title == branch.Title:
                        # A TRICK! A FEATURE!
                        # If the page shares the same Title as the section it is in then omit it
                        # from the menu - the section link will serve.
                        continue
                    pages.append({"url": url, "title": page.Title})
                branch_nodes.append({"url": first_page_url, "title": branch.Title, "pages": pages})
            tree.extend(branch_nodes)
        return tree


class AddForm(base.AddForm):
    form_fields = form.Fields(INavigationPortlet)
    label = u"Add TCAA Navigation portlet"
    description = u"Display full tree navigation as needed by tcaa theme"

    # object contruction handler
    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment


class EditForm(base.EditForm):
    form_fields = form.Fields(INavigationPortlet)
    label = u"Edit TCAA Navigation portlet"
    decription = u"Display full tree navigation as needed by tcaa theme"

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
from zope.component import getMultiAdapter
from zope.component import queryUtility

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.registry.interfaces import IRegistry
from plone.portlets.interfaces import IPortletDataProvider

from Products.ATContentTypes.interfaces.link import IATLink
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from tcaa.content.interfaces import ITCAAContentish
from tcaa.content.interfaces import ITCAASettings
from tcaa.content.section import ISection
from tcaa.content.basepage import IBasePage


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

    def __init__(self,count=4):
        self.count = count

    title = u"TCAA Navigation"


# View class
class Renderer(base.Renderer):

    # render() will be called to render the portlet
    render = ViewPageTemplateFile('navigation.pt')

    # Always available
    def available(self):
        return True

    def tree(self):
        """
        """
        #pageData = getMultiAdapter((self.context, self.request), name="pagedata")
        #return pageData.createTree()
        return self._data()

    def _get_tcaa_settings(self):
        registry = queryUtility(IRegistry)
        if registry is None:
            return None 
        return registry.forInterface(ITCAASettings, check=False)
         
    @memoize
    def twitter_feed(self):
        settings = self._get_tcaa_settings()
        if settings == None:
            return ''
        return "http://api.twitter.com/1/statuses/user_timeline.json?screen_name=%s&callback=twitterCallback2&count=1" % (settings.twitter_account,)
   
    @memoize
    def email(self):
        settings = self._get_tcaa_settings()
        if settings == None:
            return '#'
        return 'mailto:%s' % (settings.email_account or '')
    
    @memoize
    def facebook(self):
        settings = self._get_tcaa_settings()
        if settings == None:
            return '#'
        return 'http://www.facebook.com/%s' % (settings.facebook_account or '')

    @memoize
    def linkedin(self):
        settings = self._get_tcaa_settings()
        if settings == None:
            return '#'
        return 'http://www.linkedin.com/%s' % (settings.linkedin_account or '')

    @memoize
    def twitter(self):
        settings = self._get_tcaa_settings()
        if settings == None:
            return '#'
        return 'http://twitter.com/#!/%s' % (settings.twitter_account or '')

    @memoize
    def _data(self):
        pc = getToolByName(self.context, 'portal_catalog')
        pu = getToolByName(self.context, 'portal_url')
        portal = pu.getPortalObject()
        path = portal.getPhysicalPath()
        q = {'path': {'query': '/'.join(path), 'depth':1},
             'review_state' : 'published',
             'sort_on': 'getObjPositionInParent',
             'object_provides':(ITCAAContentish.__identifier__, IATLink.__identifier__,),
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
                q['path'] = {'query': '/'.join(path), 'depth':1}
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
                branch_nodes.append({"url":first_page_url, "title":branch.Title, "pages":pages})
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



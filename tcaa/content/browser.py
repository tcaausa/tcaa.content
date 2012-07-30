
import json
from five import grok
from Acquisition import aq_inner, aq_parent
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from tcaa.content.interfaces import ITCAAContentish
from tcaa.content.section import ISection
from tcaa.content.basepage import IBasePage


class View(grok.View):
    """Default view for TCAA content which handles XMLHttpRequests

    The associated template is found in browser_templates/view.pt
    and it makes use of the @@fragment view
    """
    
    grok.context(ITCAAContentish)
    grok.require('zope2.View')
    grok.name('view')

    def __call__(self):
        if self.request.environ.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            fragment_view = getMultiAdapter((self.context, self.request), name="fragment")
            return fragment_view()
        return super(View, self).__call__()


class ContactSubmit(grok.View):
    """Contact form async handler"""
    grok.context(ITCAAContentish)
    grok.require('zope2.View')
    grok.name('contact_submit')

    def update(self):
        # validate
        putils = getToolByName(self, 'plone_utils')

        self.c_name = self.request.form.get('name')
        self.c_email = self.request.form.get('email')
        self.c_message = self.request.form.get('message')
        self.errors = []
        if not self.c_name:
            self.errors.append({'inputerror':'name missing'})
        if not self.c_email or not putils.validateEmailAddresses(self.c_email):
            self.errors.append({'inputerror':'email missing or invalid'})
        if not self.c_message:
            self.errors.append({'inputerror':'message missing'})
            
        if self.errors:
            self.retval = {'errors': self.errors}
            return

        #process
        self.sendContactMail()
        self.retval = {'errors': self.errors}

    def render(self):
        if self.request.environ.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return json.dumps(self.retval)
        return "You cannot use this resource directly"

    def sendContactMail(self):
        portal = getToolByName(self, 'portal_url').getPortalObject()
        putils = getToolByName(self, 'plone_utils')
        envelope_from = portal.getProperty('email_from_address')
        envelope_to = envelope_from 
        send = portal.getProperty('email_from_name')
        message = """Contact from %s 
        email: %s 
        message:
        %s""" % (self.c_name, self.c_email, self.c_message)
        subject = "Contact from TCAAUSA website"
        try:
            host = putils.getMailHost()
            result = host.send(message, mto=envelope_to, mfrom=envelope_from, subject=subject)
        except Exception as e:
            self.errors.append({'exception':'There was a problem sending your contact details.'})
            context.plone_log("ContactSubmit: %s" % e)
            

class PageData(grok.View):
    """Utility view that builds the page data json object
    
    It is available for all contexts.
    """

    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('pagedata')

    def update(self):
        self.pagedata = self.getPageData()

    def render(self):
        return '<script type="text/javascript">var pageData = %s;</script>' % self.pagedata

    @memoize
    def getPageData(self):
        return json.dumps(self.createTree())
    
    @memoize
    def createTree(self):
        pc = getToolByName(self.context, 'portal_catalog')
        pu = getToolByName(self.context, 'portal_url')
        portal = pu.getPortalObject()
        path = portal.getPhysicalPath()
        q = {'path': {'query': '/'.join(path), 'depth':1},
             'review_state' : 'published',
             'sort_on': 'getObjPositionInParent',
             'object_provides':ITCAAContentish.__identifier__,
             }
        tree = []
        results = pc(q)
        for branch in results:
            branch_nodes = []
            if branch.portal_type != 'tcaa.content.Section':
                url = "/%s" % (branch.id)
                branch_nodes.append({"url": url, "title": branch.Title})
            else:
                path = list(portal.getPhysicalPath())
                path.append(branch.id)
                q['path'] = {'query': '/'.join(path), 'depth':1}
                nodes = pc(q)
                for node in nodes:
                    url = "/%s/%s" % (branch.id, node.id)
                    branch_nodes.append({"url": url, "title": node.Title})
            tree.append(branch_nodes)
        return tree

class SectionSiblings(grok.View):

    grok.context(IBasePage)
    grok.require('zope2.View')
    grok.name('section-siblings')

    def update(self):
        """Check that the context is within a Section and return siblings
        Otherwise return an empty list
        """
        parent = aq_parent(self.context)
        if ISection.providedBy(parent):
            self.siblings = self.getSiblings()
        else:
            context = aq_inner(self.context)
            url = "/%s" % (context.id,)
            self.siblings = [{"url":url, "title":context.Title(), "current":True}]

    def render(self):
        return self.siblings

    def getSiblings(self):
        pc = getToolByName(self.context, 'portal_catalog')
        context = aq_inner(self.context)
        parent = aq_parent(self.context)
        path = parent.getPhysicalPath()
        q = {'path': {'query': '/'.join(path), 'depth': 1},
             'review_state': 'published',
             'sort_on': 'getObjPositionInParent',
             'object_provides':ITCAAContentish.__identifier__,
             }
        results = pc(q)
        siblings = []
        for sibling in results:
            url = "/%s/%s" % (parent.id, sibling.id)
            data = {"url": url, "title": sibling.Title, "current": sibling.id == context.id }
            siblings.append(data)
        return siblings

class CustomPageStyle(grok.View):
    """Helper view for IBasePage implementors that
    will generate the right styling for their containing div
    when running through Diazo or direct to the admin interface.
    """
    grok.context(IBasePage)
    grok.require('zope2.View')
    grok.name('custom-page-style')

    def update(self):
        context = aq_inner(self.context)
        scales = getMultiAdapter((context, self.request), name='images')
        scale = scales.scale('backgroundImage', width=2000, height=568)

        if scale is None and context.pageBackgroundColor == '':
            self.style = None
            return

        self.style = "height:533px; padding:35px 17px 0 220px;"
        bg_img = ''
        bg_color = ''
        if scale:               
            bg_img = "url(%s) no-repeat 0 0" % (scale.url)
        if context.pageBackgroundColor:
            bg_color = "#%s" % context.pageBackgroundColor
        self.style = "%s background:%s %s;" % (self.style, bg_img, bg_color)
               
    def render(self):
        return self

    def page_style(self):
        return self.style

    def content_style(self):
        return None

    def content_class(self):
        context = aq_inner(self.context)
        element_class = ''

        # Depreciated as the css always sets the text to white
        #if context.whiteText:
        #    element_class += "white-text ";

        if context.textBackground:
            element_class += "text-background ";
        return element_class


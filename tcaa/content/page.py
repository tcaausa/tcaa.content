# $Id$

"""
TCAA Page

A standard page on the site
"""

__author__ = 'Pat Smith <pat.smith@isotoma.com>'
__docformat__ = 'restructuredtext en'
__version__ = '$Revision$'[11:-2]


from five import grok

from tcaa.content.basepage import IBasePage 

class IPage(IBasePage):
    """Describes a page

    We mix in IImageScaleTraversable so that we can use the @@images view to
    look up scaled versions of the 'image' field
    """


class Fragment(grok.View):
    """A view that returns the markup fragment for a page. Can
    be called directly or by used in another view.

    The associated template is found in page_templates/fragment.pt
    """
    grok.context(IPage)
    grok.require('zope2.View')
    grok.name('fragment')


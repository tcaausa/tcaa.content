# $Id$

"""
TCAA Section 

A container for pages on the site
"""

__author__ = 'Pat Smith <pat.smith@isotoma.com>'
__docformat__ = 'restructuredtext en'
__version__ = '$Revision$'[11:-2]

from five import grok
from zope import schema
from plone.directives import form

from tcaa.content.interfaces import ITCAAContentish

class ISection(form.Schema, ITCAAContentish):
    """A container for pages
    """


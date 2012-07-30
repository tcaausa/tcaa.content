# $Id$

"""
TCAA base page 
"""
__author__ = 'Pat Smith <pat.smith@isotoma.com>'
__docformat__ = 'restructuredtext en'
__version__ = '$Revision$'[11:-2]


from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage
from plone.app.textfield import RichText
from tcaa.content.interfaces import ITCAAContentish
from plone.z3cform.textlines.textlines import TextLinesFieldWidget

content_layout_options = SimpleVocabulary(
        [SimpleTerm(value=u"content-left",          title=u"Align Left"),
         SimpleTerm(value=u"content-right",         title=u"Align Right"),
         SimpleTerm(value=u"content-bottom-left",   title=u"Bottom Left"),
         SimpleTerm(value=u"content-bottom-right",  title=u"Bottom Right"),
         SimpleTerm(value=u"content-wide",          title=u"Fill width"),]
    )


class IBasePage(form.Schema, IImageScaleTraversable, ITCAAContentish):
    """Describes a page

    We mix in IImageScaleTraversable so that we can use the @@images view to
    look up scaled versions of the 'image' field
    """

    content = RichText(
            title=u"Content",
            description=u"Rich text for page",
            required=False,
        )

    content_layout = schema.Choice(
            title=u"Content Layout",
            description=u"Position at which the above text content should be displayed",
            vocabulary=content_layout_options,
        )

    borderColor = schema.TextLine(
            title=u"Content Border Color",
            description=u"A hex value for the border color of text on this page e.g. '3fe3b2'. Leave blank for no border.",
            required=False,
        )
    backgroundColor = schema.TextLine(
            title=u"Content Background Color",
            description=u"A hex value for the background color of text on this page e.g. '3fe3b2'. Leave blank for a transparent background.",
            required=False,
        )

    whiteText = schema.Bool(
            title=u"White Text",
            description=u"Check this to make text content white",
            required=False,
        )
    pageBackgroundColor = schema.TextLine(
            title=u"Page Background Color",
            description=u"a hex value for the background color the page. Leave blank for default.",
            required=False,
        )

    backgroundImage = NamedBlobImage(
            title=u"Page Background Image (2000 x 568)",
            description=u"An image used for the background of this page",
            required=False,
        )
    navigationImage = NamedBlobImage(
            title=u"Navigation Image (282 x 224)",
            description=u"An image used on other pages when linking to this page",
            required=False,
        )
    textBackground = schema.Bool(
            title=u"Text background",
            description=u"Check this to show the grey background on body text and headlines",
            required=False,
            default=True,
        )


    form.fieldset('seo',
            label=u"SEO Options",
            fields=['metaTitle', 'metaDescription','metaKeywords'],
            )
    metaTitle = schema.TextLine(
            title=u"Meta Title",
            description=u"Content of the meta:title tag for this page",
            required=False,
            )
    metaDescription = schema.TextLine(
            title=u"Meta Description",
            description=u"Content of the meta:description tag for this page",
            required=False,
            )
    metaKeywords = schema.TextLine(
            title=u"Meta Keywords",
            description=u"Content of the meta:keywords tag for this page - a comma separated list",
            required=False,
            )
   
    # Depricated fields:
    form.omitted('content_layout')
    form.omitted('borderColor')
    form.omitted('backgroundColor')
    form.omitted('whiteText')



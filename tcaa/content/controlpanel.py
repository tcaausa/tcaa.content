from plone.z3cform import layout

from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from tcaa.content.interfaces import ITCAASettings

class TCAAControlPanelForm(RegistryEditForm):
    schema = ITCAASettings

    label = u"TCAA control panel"

TCAAControlPanelView = layout.wrap_form(TCAAControlPanelForm, ControlPanelFormWrapper)

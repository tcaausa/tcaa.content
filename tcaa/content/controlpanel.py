from plone.z3cform import layout

from zope.component import queryUtility
from zope.interface import implements
from plone.registry.interfaces import IRegistry
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from tcaa.content.interfaces import ITCAASettings


class TCAAControlPanelForm(RegistryEditForm):
    schema = ITCAASettings

    label = u"TCAA control panel"

TCAAControlPanelView = layout.wrap_form(TCAAControlPanelForm, ControlPanelFormWrapper)


class TCAASettings(object):
    """ Facade for accessing our own portal registry settings """

    implements(ITCAASettings)

    def __init__(self):
        self._settings = self._readRegistrySettings()

    def _readRegistrySettings(self):
        registry = queryUtility(IRegistry)
        if registry is None:
            return None
        return registry.forInterface(ITCAASettings, check=False)

    def forName(self, name, default=None):
        if self._settings and hasattr(self._settings, name):
            return getattr(self._settings, name)
        return default

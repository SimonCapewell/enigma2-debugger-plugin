# GUI (Screens)
from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen

# GUI (Summary)
from Screens.Setup import SetupSummary

# GUI (Components)
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.Boolean import Boolean

# Configuration
from Components.config import config, getConfigListEntry
from Components.PluginComponent import plugins
from Tools.Directories import resolveFilename, SCOPE_PLUGINS


class DebuggerSetup(Screen, ConfigListScreen):
	skin = """<screen name="DebuggerSetup" position="center,center" size="565,370">
		<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />
		<widget source="key_red" render="Label" position="0,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget source="key_green" render="Label" position="140,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
		<widget name="config" position="5,50" size="555,250" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/div-h.png" position="0,301" zPosition="1" size="565,2" />
		<widget source="help" render="Label" position="5,305" size="555,63" font="Regular;21" />
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.skinName = [self.skinName, "Setup"]
		self["HelpWindow"] = Pixmap()
		self["HelpWindow"].hide()
		self["VKeyIcon"] = Boolean(False)
		self['footnote'] = Label("")
		self["description"] = Label()

		# Summary
		self.setup_title = _("Debugger Setup")
		Screen.setTitle(self, _(self.setup_title))
		self.onChangedEntry = []

		ConfigListScreen.__init__(self, [], session = session, on_change = self.changedEntry)
		self.createConfig()

		self["actions"] = ActionMap(["SetupActions", 'ColorActions'],
		{
			"red": self.cancel,
			"green": self.save,
			"save": self.save,
			"cancel": self.cancel,
			"ok": self.save,
		}, -2)
		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("OK"))

	def createConfig(self):
		configList = [
			getConfigListEntry(_("Debugpy Start Mode"), config.plugins.debugger.debugpy_start_mode, _("Control when the debugpy server is launched.")),
			getConfigListEntry(_("Debugpy Port"), config.plugins.debugger.debugpy_port, _("Set the port that debugpy listens for clients on."))
		]
		self["config"].setList(configList)
		if config.usage.sort_settings.value:
			self["config"].list.sort()

	def updateConfig(self, configElement):
		self.createConfig()

	# for summary:
	def changedEntry(self):
		for x in self.onChangedEntry:
			x()
	def getCurrentEntry(self):
		return self["config"].getCurrent()[0]
	def getCurrentValue(self):
		return str(self["config"].getCurrent()[1].getText())
	def createSummary(self):
		from Screens.Setup import SetupSummary
		return SetupSummary

	def save(self):
		self.saveAll()
		plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
		self.close()

	def cancel(self):
		self.keyCancel()

	def createSummary(self):
		return SetupSummary

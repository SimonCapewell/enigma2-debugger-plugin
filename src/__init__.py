from Components.config import config, ConfigSubsection, ConfigSelection, ConfigSelectionNumber, ConfigYesNo

config.plugins.debugger = ConfigSubsection()
config.plugins.debugger.debugpy_start_mode = ConfigSelection(default = "0", choices = [("0", _("Manual")), ("1", _("At boot time")), ("2", _("At boot time then wait for debug client"))])
config.plugins.debugger.debugpy_port = ConfigSelectionNumber(5000, 9999, 1, default = 9998)

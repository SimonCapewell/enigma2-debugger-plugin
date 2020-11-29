from __future__ import print_function
import os
import sys
from Components.About import about
from Components.config import config
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox

from DebuggerSetup import DebuggerSetup

isListening = False

def startListening():
	global isListening
	if isListening:
		return True

	try:
		network = about.getIfConfig("eth0") or about.getIfConfig("eth1") or about.getIfConfig("wlan0")
		if not network or not network.has_key("addr"):
			return False
		sys.argv = [] # debugpy.listen crashes without this
		import debugpy
		debugpy.listen((network["addr"], config.plugins.debugger.debugpy_port.value))
		isListening = True
		print("[PythonDebug] Debug server listening on %s:%d" % (network["addr"], config.plugins.debugger.debugpy_port.value))
		return True
	except Exception as error:
		print("[PythonDebug] Failed to start debug server %s" % error)
		return False

def waitForClientConnect():
	try:
		import debugpy
		print("[PythonDebug] Waiting for a debugger client to connect")
		debugpy.wait_for_client()
		debugpy.breakpoint()
	except Exception as error:
		print("[PythonDebug] Failed wait for debugger client %s" % error)

def stopListening():
	global isListening
	if not isListening:
		return True

	try:
		import pydevd
		pydevd.stoptrace()
		isListening = False
		print("[PythonDebug] Debug server stopped")
		return True
	except Exception as error:
		print("[PythonDebug] Failed to stop debug server %s" % error)
		return False

def start(session, **kwargs):
	if not startListening() and session:
		session.open(MessageBox, "Failed to start debugpy server.", MessageBox.TYPE_ERROR)

def stop(session, **kwargs):
	if not stopListening() and session:
		session.open(MessageBox, "Failed to stop debugpy server.", MessageBox.TYPE_ERROR)

def sessionStart(reason, session, **kwargs):
	if reason != 0:
		return
	startMode = os.environ.get("ENIGMA_DEBUGPY_START_MODE") or config.plugins.debugger.debugpy_start_mode.value
	if startMode is None or startMode == "0":
		return
	if startListening():
		if startMode == "2":
			waitForClientConnect()
	elif session:
		session.open(MessageBox, "Failed to start debug server.", MessageBox.TYPE_ERROR)

def setup(session, **kwargs):
	session.open(DebuggerSetup)

def Plugins(**kwargs):
	global isListening
	pluginList = [
		PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=sessionStart),

		PluginDescriptor(
			name=_("Python Debugger Setup"), 
			description=_("Setup the debugpy server"), 
			where=[PluginDescriptor.WHERE_EXTENSIONSMENU],
			fnc=setup,
			needsRestart=False),

		PluginDescriptor(
			name=_("Python Debugger: Start"), 
			description=_("Start the debugpy server"), 
			where=[PluginDescriptor.WHERE_EXTENSIONSMENU],
			fnc=start,
			needsRestart=False),

		PluginDescriptor(
			name=_("Python Debugger: Stop"),
			description=_("Stop the debugpy server"),
			where=[PluginDescriptor.WHERE_EXTENSIONSMENU],
			fnc=stop,
			needsRestart=False)
	]

	return pluginList

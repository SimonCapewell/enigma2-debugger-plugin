from enigma import eTimer
from twisted.internet import inotify
from twisted.python import filepath

import skin
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN


class SkinAutoReloader(object):
	instance = None

	@staticmethod
	def start(session, **kwargs):
		if not SkinAutoReloader.instance:
			SkinAutoReloader.instance = SkinAutoReloader(session)

	@staticmethod
	def stop(session, **kwargs):
		if SkinAutoReloader.instance:
			print("[SkinAutoReloader] Stopping watching for skin changes")
			SkinAutoReloader.instance = None
			
	def __init__(self, session):
		watchPath = resolveFilename(SCOPE_CURRENT_SKIN, "")
		print("[SkinAutoReloader] Starting watching for skin changes in %s" % watchPath)
		self.session = session
		self.bounceTimer = None
		self.notifier = inotify.INotify()
		self.notifier.startReading()
		self.notifier.watch(filepath.FilePath(watchPath), mask=inotify.IN_MODIFY,
			callbacks=[self.__notify], recursive=True)

	def __notify(self, ignored, filepath, mask):
		if self.bounceTimer:
			return
		file, ext = filepath.splitext()
		print("[SkinAutoReloader] Detected a change to %s%s" % (file, ext))
		if ext == b".xml":
			self.bounceTimer = eTimer()
			self.bounceTimer.callback.append(self.__reloadSkin)
			self.bounceTimer.start(500, True)

	def __reloadSkin(self):
		print("[SkinAutoReloader] Reloading skin")
		def reloadComplete():
			skin.removeOnLoadCallback(reloadComplete)
			self.bounceTimer = None

		skin.addOnLoadCallback(reloadComplete)
		self.session.reloadSkin()

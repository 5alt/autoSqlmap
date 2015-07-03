# -*- coding: utf-8 -*-
from Queue import Empty
import multiprocessing 
import time
import sys

from lib.sqlmapapiwrapper import SqlmapAPIWrapper
import config

def with_color(c, s):
	return "\x1b[%dm%s\x1b[0m" % (c, s)

class myinjector():
	def run(self):
		while True:
			try:
				(fname,taskid,url) = config.queue.get(timeout=1)
				injector = SqlmapAPIWrapper(fname)
				injector.settaskid(taskid)

				if not injector.terminal():
					config.queue.put((fname,taskid,url))
					time.sleep(3)
					continue

				if injector.vulnerable():
					print with_color(32, "#%s [VulUrl] %s"%(time.strftime("%H:%M:%S"),url))
					print with_color(32, "#%s [Exploit] sqlmap -r %s"%(time.strftime("%H:%M:%S"), config.save_path + '/' + fname))
					sys.stdout.flush()
					injector.delete()
				else:
					injector.clear()
			except Empty:
				time.sleep(3)
			except KeyboardInterrupt:
				return
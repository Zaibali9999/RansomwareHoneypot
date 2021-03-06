import time
import sys
import os
import subprocess
import re

import psutil

import config

class Monitor(object):
	# Initialization for Monitor Class
	def __init__(self, regex=None):
		self.config = config.configuration
		self.current_path = os.path.dirname(os.path.realpath(__file__))
		if regex != None:
			self.regex = regex
			self.regex_object = re.compile(self.regex, re.IGNORECASE)
		else:
			self.regex = r".*" + re.escape("sample") + r".*"
			self.regex_object = re.compile(self.regex, re.IGNORECASE)
		return

	# function that monitors files open
	def monitor_processlist(self):
		"""
		"""
		for proc in psutil.process_iter():
			try:
				pinfo = proc.as_dict(attrs=['pid'])
				proci = psutil.Process(pinfo['pid'])
				for files in proci.open_files() :
					match = self.regex_object.search(str(files))
					if match is not None:

						print "[+] File being accessed at " + time.ctime() + " by process " + str(pinfo['pid'])
						print "[+] Process with PID: " + str(pinfo['pid']) + " is suspended for memory imaging."

						dumpcmd = self.config['package_externals_path'] + '\MemoryDD.bat -output ' + self.config['package_dump_path']	

						#subprocess.check_call(dumpcmd, "", stdin=None, stdout=None, stderr=None, shell=False)
						
						p = subprocess.check_call(dumpcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

						return True	
			except psutil.NoSuchProcess:
				pass
			except psutil.AccessDenied:
				pass
			except Exception as e:
				print "[-] Unknown exception has occured. Restarting monitor."
				pass

		return False

	def initialize(self):
		""" Starts an infinte loop that monitors files open by a process
		"""
		while True:
			status = self.monitor_processlist()
			if status == True:
				break
		return True

def main():
	""" Function used for testting
	"""
	monitor_object = Monitor()
	monitor_object.intialize()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt as e:
		print e
		print 'Exiting Monitor.'
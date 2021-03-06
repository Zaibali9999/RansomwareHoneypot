import time
import os
import hashlib

import fnmatch

import config

class Report(object):

	def __init__(self):
		self.config = config.configuration

	def generate_report(self):
		file_found_status = False
		file_location = ""
		while(not file_found_status):
			time.sleep(1)
			for root, dirnames, filenames in os.walk(self.config['package_dump_path']):
				for filename in fnmatch.filter(filenames, '*.img'):
					file_location = os.path.join(root, filename)
					file_found_status = True

		print "[+] File image saved to: " + file_location
		print "[+] Report generated."

		report_location = self.config['package_path'] + self.config['separator'] + "report.txt"
		report_file = open(report_location, "w")

		report_file.write("FINAL YEAR PROJECT \n")

		report_file.write("Image Location: " + file_location + '\n')
		report_file.write("Report Location: " + report_location + '\n')

		print "[+] Report saved to: " + report_location

	def generate_text_report(self):
		return
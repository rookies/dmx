#!/usr/bin/python3
from Exceptions import DeviceFileException

class Channel(object):
	def fromEtree(self, etree):
		## Get children (value) ##
		for child in etree:
			## Check element ##
			if child.tag != "value":
				raise DeviceFileException("Channel child tag must be named value.")
			if not "start" in child.attrib:
				raise DeviceFileException("Channel child tag must have start attribute.")
			## Get attributes ##
			if "variation" in child.attrib:
				self.addValue(child.attrib["start"], child.text, child.attrib["variation"])
			else:
				self.addValue(child.attrib["start"], child.text, None)

class Color(Channel):
	def addValue(self, start, value, variation):
		pass #TODO#

class Shutter(Channel):
	def addValue(self, start, value, variation):
		pass #TODO#

class Gobo(Channel):
	def addValue(self, start, value, variation):
		pass #TODO#

class GoboRotation(Channel):
	def addValue(self, start, value, variation):
		pass #TODO#

class Prism(Channel):
	def addValue(self, start, value, variation):
		pass #TODO#

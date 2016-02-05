#!/usr/bin/python3
import logging
import xml.etree.ElementTree as ET
import DeviceChannels
from Exceptions import DeviceFileException

class Device(object):
	devType = "undefType"
	devName = "undefName"
	devVendor = "undefVend"
	devProfiles = {}
			
	def __str__(self):
		return "[Device] %s %s (%s) with %d profile(s): %s" % (
			self.devVendor,
			self.devName,
			self.devType,
			len(self.devProfiles),
			self.devProfiles
		)
	
	def fromFile(self, f):
		## Parse XML ##
		logging.info("Reading from file `%s'.", f)
		tree = ET.parse(f)
		root = tree.getroot()
		## Check root element (device) ##
		if root.tag != "device":
			raise DeviceFileException("Root tag must be named device.")
		for attr in ["type","name","vendor"]:
			if not attr in root.attrib:
				raise DeviceFileException("Root tag must have %s attribute." % attr)
		self.devType = root.attrib["type"]
		self.devName = root.attrib["name"]
		self.devVendor = root.attrib["vendor"]
		## Get children (profile) ##
		for child in root:
			## Check element ##
			if child.tag != "profile":
				raise DeviceFileException("Child tag must be named profile.")
			if not "name" in child.attrib:
				raise DeviceFileException("Child tag must have name attribute.")
			## Check name ##
			profName = child.attrib["name"]
			if profName in self.devProfiles.keys():
				raise DeviceFileException("Profile named %s already exists." % profName)
			## Add profile ##
			prof = DeviceProfile()
			prof.fromEtree(child)
			self.devProfiles[profName] = prof
	
class DeviceProfile(object):
	profChannels = {}
	
	def fromEtree(self, etree):
		## Get children (channel) ##
		for child in etree:
			## Check element ##
			if child.tag != "channel":
				raise DeviceFileException("Profile child tag must be named channel.")
			for attr in ["offset","name"]:
				if not attr in child.attrib:
					raise DeviceFileException("Profile child tag must have %s attribute." % attr)
			## Check name ##
			cName = child.attrib["name"]
			if cName in self.profChannels.keys():
				raise DeviceFileException("Channel named %s already exists." % cName)
			## Add channel ##
			if cName in ["pan","finepan","tilt","finetilt","acuity"]:
				## Channels without class ##
				cObject = None
			elif cName in ["color","shutter","gobo","gobo_rotation","prism"]:
				## Channels with class ##
				if cName == "color":
					cObject = DeviceChannels.Color()
				elif cName == "shutter":
					cObject = DeviceChannels.Shutter()
				elif cName == "gobo":
					cObject = DeviceChannels.Gobo()
				elif cName == "gobo_rotation":
					cObject = DeviceChannels.GoboRotation()
				elif cName == "prism":
					cObject = DeviceChannels.Prism()
				else:
					raise Exception("Unhandled case.")
				cObject.fromEtree(child)
			else:
				## Unsupported channels ##
				raise DeviceFileException("Channel named %s not supported yet, sorry." % cName)
			self.profChannels[cName] = (int(child.attrib["offset"]),cObject)
		print(self.profChannels)

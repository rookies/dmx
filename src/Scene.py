#!/usr/bin/python3
import logging
import xml.etree.ElementTree as ET
from Exceptions import SceneFileException
import SceneCommands

class Scene(object):
	metaData = {}
	commands = {}
	
	def fromFile(self, f):
		## Parse XML ##
		logging.info("Reading from scene file `%s'.", f)
		tree = ET.parse(f)
		root = tree.getroot()
		## Check root element (scene) ##
		if root.tag != "scene":
			raise SceneFileException("Root tag must be named scene.")
		## Get children ##
		for child in root:
			## Check element name ##
			if child.tag == "meta":
				if "key" in child.attrib:
					key = child.attrib["key"]
					if key in self.metaData:
						raise SceneFileException("MetaData key already exists: %s." % key)
					else:
						self.metaData[key] = child.text
				else:
					raise SceneFileException("Meta tag must have key attribute.")
			elif child.tag == "command":
				if ("start" in child.attrib) and ("value" in child.attrib):
					key = int(child.attrib["start"])
					if not key in self.commands:
						self.commands[key] = []
					self.commands[key].append(SceneCommands.Helpers.get(child.attrib["value"]))
				else:
					raise SceneFileException("Command tag must have start and value attributes.")
			else:
				raise SceneFileException("Child tag must be named meta or command, not ." % child.tag)
	def getDuration(self):
		dur = 0
		for l in self.commands.items():
			for c in l[1]:
				tmp = l[0] + c.getDuration()
				if tmp > dur:
					dur = tmp
		return dur

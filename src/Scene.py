#!/usr/bin/python3
import logging
import xml.etree.ElementTree as ET
from Exceptions import SceneFileException

class Scene(object):
	metaData = {}
	commands = []
	
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
					if key in self.metaData.keys():
						raise SceneFileException("MetaData key already exists: %s." % key)
					else:
						self.metaData[key] = child.text
				else:
					raise SceneFileException("Meta tag must have key attribute.")
			elif child.tag == "command":
				if ("start" in child.attrib) and ("value" in child.attrib):
					self.commands.append(
						SceneCommand(int(child.attrib["start"]), child.attrib["value"])
					)
				else:
					raise SceneFileException("Command tag must have start and value attributes.")
			else:
				raise SceneFileException("Child tag must be named meta or command, not ." % child.tag)
		## Dump content ##
		print(self.metaData)
		for cmd in self.commands:
			print(cmd)

class SceneCommand(object):
	cStart = 0
	cValue = 0
	
	def __str__(self):
		return "[SceneCommand] @ %dms: %s" % (self.cStart, self.cValue)
	
	def __init__(self, start, value):
		self.cStart = start
		self.cValue = value

#!/usr/bin/python3
import random #FIXME#

class Helpers(object):
	@staticmethod
	def get(value):
		## Split cmd and args ##
		if value.find("|") == -1:
			cmd = value
		else:
			v = value.split("|")
			cmd = v[0]
			args = v[1:]
		## Check command ##
		if cmd == "set":
			return Set(args)
		elif cmd == "fade":
			return Fade(args)
		elif cmd == "wait":
			return Wait(args)
	@staticmethod
	def parseValue(value):
		v = int(value)
		if (v < 0) or (v > 255):
			raise ValueError("Value must be between 0 and 255.")
		return v

class Command(object):
	def maintain(self, t):
		# Return values:
		## 0: not done
		## 1: done
		## 2: stop clock
		print("FIXME: No maintain(t) method defined for %s." % self)
		return 0
	
class Set(Command):
	channel = None
	value = 0
	
	def __str__(self):
		return "Set(channel='%s',value=%d)" % (self.channel, self.value)
	
	def __init__(self, args):
		if len(args) is not 2:
			raise SceneError("Set command needs exactly two parameters.")
		self.channel = args[0]
		self.value = Helpers.parseValue(args[1])
		
	def maintain(self, t):
		#TODO#
		return 1 #done#

class Fade(Command):
	channel = None
	value = 0
	duration = 0
	
	def __str__(self):
		return "Fade(channel='%s',value=%d,duration=%dms)" % (self.channel, self.value, self.duration)
	
	def __init__(self, args):
		if len(args) is not 3:
			raise SceneError("Fade command needs exactly three parameters.")
		self.channel = args[0]
		self.value = Helpers.parseValue(args[1])
		self.duration = int(args[2])
		
	def maintain(self, t):
		#TODO#
		if t >= self.duration:
			return 1 #done#
		else:
			return 0 #not done#
	
class Wait(Command):
	action = None
	
	def __str__(self):
		return "Wait(action='%s')" % self.action
	
	def __init__(self, args):
		if len(args) is not 1:
			raise SceneError("Wait command needs exactly one parameters.")
		self.action = args[0]
		
	def maintain(self, t):
		if random.randint(0,5) == 1:
			return 1 #done#
		else:
			return 2 #stop clock#

class SceneError(Exception):
	pass

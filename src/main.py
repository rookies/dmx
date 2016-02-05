#!/usr/bin/python3
import sys, logging
from Device import Device

logging.basicConfig(level=logging.DEBUG)
d = Device()
#print(d)
d.fromFile(sys.argv[1])
#print(d)

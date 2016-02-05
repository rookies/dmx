#!/usr/bin/python3
import sys, logging
from Scene import Scene

logging.basicConfig(level=logging.DEBUG)
s = Scene()
s.fromFile(sys.argv[1])

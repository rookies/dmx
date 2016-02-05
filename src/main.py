#!/usr/bin/python3
import sys, logging, time
from Scene import Scene

logging.basicConfig(level=logging.DEBUG)
s = Scene()
s.fromFile(sys.argv[1])
running = []
times = sorted(s.commands.keys())
t = 0
while t < 5000:
	## Check if we reached a new command ##
	if (len(times) > 0) and (t >= times[0]):
		for c in s.commands[times[0]]:
			print("%10dms: BEG: %s" % (t, c))
			running.append((t, c))
		times.pop(0)
	## Maintain running commands ##
	stillRunning = []
	for c in running:
		res = c[1].maintain(t-c[0])
		if res == 0:
			stillRunning.append(c)
		elif res == 1:
			print("%10dms: END: %s" % (t, c[1]))
		elif res == 2:
			stillRunning.append(c)
			print("%10dms: RST: %s" % (t, c[1]))
			t -= 1
		else:
			raise ValueError()
	running = stillRunning
	## Increase timer ##
	t += 1
	## FIXME: Sleep ##
	time.sleep(0.001)

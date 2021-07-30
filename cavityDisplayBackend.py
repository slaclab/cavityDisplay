from fault import *

for cavity in machine:
	cavity.addThread(updateStatus)
	cavity.launchThread

def updateStatus():
	while True:
		for fault in faults:
			if fault.isFaulted():
				fault.writeToPVs()
				break


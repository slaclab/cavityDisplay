from fault import *
from scLinac import LINACS

for linac in LINACS:
    for _, cryomodule in linac.cryomodules.items():
        for _, cavity in cryomodule.cavities.items():
            # cavity.addThread(updateStatus)
            # cavity.launchThread
            pass


def updateStatus():
    while True:
        for fault in faults:
            if fault.isFaulted():
                fault.writeToPVs()
                break


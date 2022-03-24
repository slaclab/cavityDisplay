# from epics import PV
from time import time

from displayCavity import DISPLAY_LINAC_OBJECTS

# WATCHER_PV = PV("PHYS:SYS0:1:SC_CAV_FAULT_HEARTBEAT")

while True:
    start = time()
    for linac in DISPLAY_LINAC_OBJECTS:
        for cryomodule in linac.cryomodules.values():
            for cavity in cryomodule.cavities.values():
                cavity.runThroughFaults()

    # WATCHER_PV.put(WATCHER_PV.value + 1)
    print(time() - start)

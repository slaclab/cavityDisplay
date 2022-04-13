from datetime import datetime
from time import sleep

from epics import PV

from displayCavity import DISPLAY_LINAC_OBJECTS
from utils import DEBUG, BACKEND_SLEEP_TIME

WATCHER_PV = PV("PHYS:SYS0:1:SC_CAV_FAULT_HEARTBEAT")

while True:
    start = datetime.now()
    for linac in DISPLAY_LINAC_OBJECTS:
        for cryomodule in linac.cryomodules.values():
            for cavity in cryomodule.cavities.values():
                cavity.runThroughFaults()
    if DEBUG:
        delta = (datetime.now() - start).total_seconds()
        sleep(BACKEND_SLEEP_TIME - delta if delta < BACKEND_SLEEP_TIME else 0)

    WATCHER_PV.put(WATCHER_PV.value + 1)

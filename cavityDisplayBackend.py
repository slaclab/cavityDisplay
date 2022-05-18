from datetime import datetime
from epics import PV
from time import sleep

from displayCavity import DISPLAY_CRYOMODULES
from utils import DEBUG, BACKEND_SLEEP_TIME

WATCHER_PV = PV("PHYS:SYS0:1:SC_CAV_FAULT_HEARTBEAT")

while True:
    start = datetime.now()
    for cryomodule in DISPLAY_CRYOMODULES.values():
        for cavity in cryomodule.cavities.values():
            cavity.runThroughFaults()
    if DEBUG:
        delta = (datetime.now() - start).total_seconds()
        sleep(BACKEND_SLEEP_TIME - delta if delta < BACKEND_SLEEP_TIME else 0)

    WATCHER_PV.put(WATCHER_PV.value + 1)

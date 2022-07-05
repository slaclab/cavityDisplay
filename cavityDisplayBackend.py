from datetime import datetime
from epics import PV
from time import sleep

from displayLinac import DISPLAY_CRYOMODULES, DisplayCryomodule
from lcls_tools.superconducting.scLinac import ALL_CRYOMODULES
from utils import BACKEND_SLEEP_TIME, DEBUG

WATCHER_PV = PV("PHYS:SYS0:1:SC_CAV_FAULT_HEARTBEAT")

while True:
    start = datetime.now()
    for cryomoduleName in ALL_CRYOMODULES:
        cryomodule: DisplayCryomodule = DISPLAY_CRYOMODULES[cryomoduleName]
        for cavity in cryomodule.cavities.values():
            cavity.runThroughFaults()
    if DEBUG:
        delta = (datetime.now() - start).total_seconds()
        sleep(BACKEND_SLEEP_TIME - delta if delta < BACKEND_SLEEP_TIME else 0)

    WATCHER_PV.put(WATCHER_PV.value + 1)

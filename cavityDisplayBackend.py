from datetime import datetime
from time import sleep

from epics import caget, caput

from displayLinac import DISPLAY_CRYOMODULES, DisplayCryomodule
from lcls_tools.superconducting.scLinac import ALL_CRYOMODULES
from utils import BACKEND_SLEEP_TIME, DEBUG

WATCHER_PV: str = "PHYS:SYS0:1:SC_CAV_FAULT_HEARTBEAT"
caput(WATCHER_PV, 0)

while True:
    start = datetime.now()
    for cryomoduleName in ALL_CRYOMODULES:
        cryomodule: DisplayCryomodule = DISPLAY_CRYOMODULES[cryomoduleName]
        for cavity in cryomodule.cavities.values():
            cavity.runThroughFaults()
    if DEBUG:
        delta = (datetime.now() - start).total_seconds()
        sleep(BACKEND_SLEEP_TIME - delta if delta < BACKEND_SLEEP_TIME else 0)
    
    caput(WATCHER_PV, caget(WATCHER_PV) + 1)

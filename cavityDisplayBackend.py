from datetime import datetime
from time import sleep

from lcls_tools.common.controls.pyepics.utils import PV
from lcls_tools.superconducting.sc_linac_utils import ALL_CRYOMODULES

from displayLinac import DISPLAY_CRYOMODULES, DisplayCryomodule
from utils import BACKEND_SLEEP_TIME, DEBUG

WATCHER_PV: PV = PV("PHYS:SYS0:1:SC_CAV_FAULT_HEARTBEAT")
WATCHER_PV.put(0)

while True:
    start = datetime.now()
    for cryomoduleName in ALL_CRYOMODULES:
        cryomodule: DisplayCryomodule = DISPLAY_CRYOMODULES[cryomoduleName]
        for cavity in cryomodule.cavities.values():
            cavity.run_through_faults()
    if DEBUG:
        delta = (datetime.now() - start).total_seconds()
        sleep(BACKEND_SLEEP_TIME - delta if delta < BACKEND_SLEEP_TIME else 0)

    try:
        WATCHER_PV.put(WATCHER_PV.get() + 1)
    except TypeError as e:
        print(f"Write to watcher PV failed with error: {e}")

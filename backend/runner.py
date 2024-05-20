from datetime import datetime
from time import sleep

from backend.backend_cavity import BackendCavity
from backend.backend_cryomodule import BackendCryomodule
from backend.backend_ssa import BackendSSA

from lcls_tools.common.controls.pyepics.utils import PV
from lcls_tools.superconducting.sc_linac import Machine
from lcls_tools.superconducting.sc_linac_utils import ALL_CRYOMODULES
from utils.utils import DEBUG, BACKEND_SLEEP_TIME

WATCHER_PV: PV = PV("PHYS:SYS0:1:SC_CAV_FAULT_HEARTBEAT")
WATCHER_PV.put(0)

DISPLAY_MACHINE = Machine(
    ssa_class=BackendSSA, cavity_class=BackendCavity, cryomodule_class=BackendCryomodule
)

while True:
    start = datetime.now()
    for cryomoduleName in ALL_CRYOMODULES:
        cryomodule: BackendCryomodule = DISPLAY_MACHINE.cryomodules[cryomoduleName]
        for cavity in cryomodule.cavities.values():
            cavity.run_through_faults()
    if DEBUG:
        delta = (datetime.now() - start).total_seconds()
        sleep(BACKEND_SLEEP_TIME - delta if delta < BACKEND_SLEEP_TIME else 0)

    try:
        WATCHER_PV.put(WATCHER_PV.get() + 1)
    except TypeError as e:
        print(f"Write to watcher PV failed with error: {e}")

from fault import *
from scLinac import LINACS, Cavity, Linac
from constants import STATUS_SUFFIX, SEVERITY_SUFFIX, DISPLAY_LINACS
from epics import PV



cavity = DISPLAY_LINACS[1].cryomodules["H2"].cavities[2]
cavity.runThroughFaults()
#for fault in faults:
    #print(fault.suffix + ": " + str(fault.isFaulted(cavity)))


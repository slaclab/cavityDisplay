from fault import *
from scLinac import LINACS, Cavity, Linac
from constants import STATUS_SUFFIX, SEVERITY_SUFFIX, DISPLAY_LINACS
from epics import PV




def updateStatus():
    while True:
        for fault in faults:
            if fault.isFaulted():
                fault.writeToPVs()
                break

class displayCavity(Cavity):
    def __init__(self):
        super(displayCavity, self).__init__()
        self.statusPV = PV(self.pvPrefix + STATUS_SUFFIX)
        self.severityPV = PV(self.pvPrefix + SEVERITY_SUFFIX)

    def runThroughFaults(self):
        while True:
            for fault in faults:
                if fault.isFaulted(self):
                    self.statusPV.put(fault.tlc)
                    self.severityPV.put(fault.severity)
                    break

cavity = DISPLAY_LINACS[1].cryomodules["H2"].cavities[1]
for fault in faults:
    print(fault.suffix + ": " + str(fault.isFaulted(cavity)))


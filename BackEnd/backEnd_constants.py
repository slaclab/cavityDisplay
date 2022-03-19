from fault import faults, PvInvalid
from epics import PV

import sys

sys.path.insert(0, '..')
from constants import STATUS_SUFFIX, SEVERITY_SUFFIX
from lcls_tools.devices.scLinac import LINACS, Linac, Cavity


class DisplayCavity(Cavity, object):
    def __init__(self, cavityNum, rackObject):
        super(DisplayCavity, self).__init__(cavityNum, rackObject)
        self.statusPV = PV(self.pvPrefix + STATUS_SUFFIX)
        self.severityPV = PV(self.pvPrefix + SEVERITY_SUFFIX)

        self.faultPVs = []
        for fault in faults:
            # Decided to use timeout of 0.01 seconds after some trial and error
            timeout = 0.01
            if fault.level == "RACK":
                if fault.rack != self.rack.rackName:
                    continue
                prefix = self.rack.pvPrefix
            elif fault.level == "CAV":
                prefix = self.pvPrefix
            else:
                prefix = self.cryomodule.pvPrefix

            self.faultPVs.append((fault, PV(prefix + fault.suffix,
                                            connection_timeout=timeout)))

    def runThroughFaults(self):
        isOkay = True
        invalid = False

        for fault, pv in self.faultPVs:
            try:
                if fault.isFaulted(pv):
                    isOkay = False
                    break
            except PvInvalid as e:
                print(e)
                isOkay = False
                invalid = True
                break

        if isOkay:
            self.statusPV.put("{num}".format(num=str(self.number)))
            self.severityPV.put(0)
        else:
            self.statusPV.put(fault.tlc)
            if not invalid:
                self.severityPV.put(fault.severity)
            else:
                self.severityPV.put(3)


DISPLAY_LINACS = []
for name, cryomoduleList in LINACS:
    DISPLAY_LINACS.append(Linac(name, cryomoduleList, cavityClass=DisplayCavity))

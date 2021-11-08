from scLinac import LINACS, Linac, Cavity
from fault import faults, PvInvalid
from epics import PV

import sys

sys.path.insert(0, '..')
from constants import STATUS_SUFFIX, SEVERITY_SUFFIX


class DisplayCavity(Cavity, object):
    def __init__(self, cavityNum, rackObject):
        super(DisplayCavity, self).__init__(cavityNum, rackObject)
        self.statusPV = self.pvPrefix + STATUS_SUFFIX
        self.severityPV = self.pvPrefix + SEVERITY_SUFFIX

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

    def runThroughFaults(self, caputDict):
        """
        caputDict.statusValues.append(str(self.number))
        caputDict.severityValues.append(0)
        """
        isOkay = True
        invalid = False

        caputDict.statusNames.append(self.statusPV)
        caputDict.severityNames.append(self.severityPV)

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
            caputDict.statusValues.append("{num}".format(num=str(self.number)))
            caputDict.severityValues.append(0)
        else:
            if not invalid:
                caputDict.statusValues.append(fault.tlc)
                caputDict.severityValues.append(fault.severity)
            else:
                caputDict.statusValues.append("INV")
                caputDict.severityValues.append(3)


DISPLAY_LINACS = []
for name, cryomoduleList in LINACS:
    DISPLAY_LINACS.append(Linac(name, cryomoduleList, cavityClass=DisplayCavity))

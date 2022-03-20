import sys
from epics import PV

from fault import CSV_FAULTS, Fault, PvInvalid

sys.path.insert(0, '..')
from constants import STATUS_SUFFIX, SEVERITY_SUFFIX
from lcls_tools.devices.scLinac import LINACS, Linac, Cavity
from typing import List


class DisplayCavity(Cavity, object):
    def __init__(self, cavityNum, rackObject):
        super(DisplayCavity, self).__init__(cavityNum, rackObject)
        self.statusPV = PV(self.pvPrefix + STATUS_SUFFIX)
        self.severityPV = PV(self.pvPrefix + SEVERITY_SUFFIX)

        self.faults: List[Fault] = []

        for csvFault in CSV_FAULTS:

            if csvFault["Level"] == "RACK":

                # Rack A cavities don't care about faults for Rack B and vice versa
                if csvFault["Rack"] != self.rack.rackName:
                    continue

            prefix = csvFault["PV Prefix"].format(LINAC=self.linac.name,
                                                  CRYOMODULE=self.cryomodule.name,
                                                  RACK=self.rack.rackName,
                                                  CAVITY=self.number)

            self.faults.append(Fault(tlc=csvFault["Severity"],
                                     severity=csvFault["Severity"],
                                     suffix=csvFault["PV Suffix"],
                                     okValue=csvFault["OK If Equal To"],
                                     faultValue=csvFault["Faulted If Equal To"],
                                     description=csvFault["Description"],
                                     name=csvFault["Name"], prefix=prefix))

    def runThroughFaults(self):
        isOkay = True
        invalid = False

        for fault in self.faults:
            try:
                if fault.isFaulted():
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

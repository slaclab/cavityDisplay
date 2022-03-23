from epics import PV
from typing import List

from cavityDisplayGUI import SEVERITY_SUFFIX, STATUS_SUFFIX
from Fault import Fault, PvInvalid
from constants import CSV_FAULTS
from lcls_tools.devices.scLinac import Cavity, LINAC_TUPLES, Linac


class DisplayCavity(Cavity):
    def __init__(self, cavityNum, rackObject):
        super(DisplayCavity, self).__init__(cavityNum, rackObject)
        self.statusPV = PV(self.pvPrefix + STATUS_SUFFIX)
        self.severityPV = PV(self.pvPrefix + SEVERITY_SUFFIX)

        self.faults: List[Fault] = []

        for csvFault in CSV_FAULTS:

            if csvFault["Level"] == "RACK":

                # Rack A cavities don't care about faults for Rack B and vice versa
                if csvFault["Rack"] != self.rack.rackName:
                    # Takes us to the next iteration of the for loop
                    continue

            # tested in the python console that strings without one of these
            # formatting keys just ignores them and moves on
            prefix = csvFault["PV Prefix"].format(LINAC=self.linac.name,
                                                  CRYOMODULE=self.cryomodule.name,
                                                  RACK=self.rack.rackName,
                                                  CAVITY=self.number)

            self.faults.append(Fault(tlc=csvFault["Three Letter Code"],
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


DISPLAY_LINAC_OBJECTS: List[Linac] = []
for name, cryomoduleList in LINAC_TUPLES:
    DISPLAY_LINAC_OBJECTS.append(Linac(name, cryomoduleList,
                                       cavityClass=DisplayCavity))

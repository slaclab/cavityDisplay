from collections import OrderedDict

from epics import PV
from typing import List, Tuple

from Fault import Fault, PV_TIMEOUT, PvInvalid
from cavityDisplayGUI import SEVERITY_SUFFIX, STATUS_SUFFIX
from constants import CSV_FAULTS
from lcls_tools.devices.scLinac import Cavity, Cryomodule, LINAC_TUPLES, Linac


class DisplayCavity(Cavity):
    def __init__(self, cavityNum, rackObject):
        super(DisplayCavity, self).__init__(cavityNum, rackObject)
        self.statusPV = PV(self.pvPrefix + STATUS_SUFFIX)
        self.severityPV = PV(self.pvPrefix + SEVERITY_SUFFIX)

        self.faults: OrderedDict[str, Fault] = OrderedDict()

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

            tlc = csvFault["Three Letter Code"]
            self.faults[tlc] = Fault(tlc=tlc,
                                     severity=csvFault["Severity"],
                                     suffix=csvFault["PV Suffix"],
                                     okValue=csvFault["OK If Equal To"],
                                     faultValue=csvFault["Faulted If Equal To"],
                                     description=csvFault["Description"],
                                     name=csvFault["Name"], prefix=prefix)

    def runThroughFaults(self):
        isOkay = True
        invalid = False

        for fault in self.faults.values():
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
DISPLAY_CRYOMODULES = OrderedDict()

for name, cryomoduleList in LINAC_TUPLES:
    displayLinac = Linac(name, cryomoduleList, cavityClass=DisplayCavity)
    DISPLAY_LINAC_OBJECTS.append(displayLinac)

    for cryomodule in displayLinac.cryomodules.values():
        DISPLAY_CRYOMODULES[cryomodule.name] = cryomodule

h1: Cryomodule = DISPLAY_CRYOMODULES["H1"]
h2: Cryomodule = DISPLAY_CRYOMODULES["H2"]

HL_CAVITY_NUMBER_PAIRS: List[Tuple[int, int]] = [(1, 5), (2, 6), (3, 7), (4, 8)]

# This hard coding is unfortunate, but I don't see any other way of handling the
# HL SSA PVs
for (leader, follower) in HL_CAVITY_NUMBER_PAIRS:
    ssaTLC = "SSA"
    ssaPVSuffix = "SSA:AlarmSummary.SEVR"

    leadingCavityH1 = h1.cavities[leader]
    h1.cavities[follower].faults[ssaTLC].pv = PV(leadingCavityH1.pvPrefix + ssaPVSuffix,
                                                 connection_timeout=PV_TIMEOUT)
    leadingCavityH2 = h2.cavities[leader]
    h2.cavities[follower].faults[ssaTLC].pv = PV(leadingCavityH2.pvPrefix + ssaPVSuffix,
                                                 connection_timeout=PV_TIMEOUT)

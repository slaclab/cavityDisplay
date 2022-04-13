from collections import OrderedDict
from typing import List, Tuple

from epics import PV

from Fault import Fault, PvInvalid, PV_TIMEOUT
from cavityDisplayGUI import SEVERITY_SUFFIX, STATUS_SUFFIX, DESCRIPTION_SUFFIX
from lcls_tools.devices.scLinac import Cavity, Cryomodule, LINAC_TUPLES, Linac
from utils import CSV_FAULTS, displayHash


class DisplayCavity(Cavity):
    def __init__(self, cavityNum, rackObject):
        super(DisplayCavity, self).__init__(cavityNum, rackObject)
        self.statusPV = PV(self.pvPrefix + STATUS_SUFFIX)
        self.severityPV = PV(self.pvPrefix + SEVERITY_SUFFIX)
        self.descriptionPV = PV(self.pvPrefix + DESCRIPTION_SUFFIX)

        self.faults: OrderedDict[int, Fault] = OrderedDict()
        for csvFaultDict in CSV_FAULTS:
            rack = csvFaultDict["Rack"]
            if csvFaultDict["Level"] == "RACK":

                # Rack A cavities don't care about faults for Rack B and vice versa
                if rack != self.rack.rackName:
                    # Takes us to the next iteration of the for loop
                    continue

            # tested in the python console that strings without one of these
            # formatting keys just ignores them and moves on
            prefix = csvFaultDict["PV Prefix"].format(LINAC=self.linac.name,
                                                      CRYOMODULE=self.cryomodule.name,
                                                      RACK=self.rack.rackName,
                                                      CAVITY=self.number)

            tlc = csvFaultDict["Three Letter Code"]
            okCondition = csvFaultDict["OK If Equal To"]
            faultCondition = csvFaultDict["Faulted If Equal To"]

            key = displayHash(rack=rack,
                              faultCondition=faultCondition,
                              okCondition=okCondition,
                              tlc=tlc)

            # setting key of faults dictionary to be row number b/c it's unique (i.e. not repeated)
            self.faults[key] = Fault(tlc=tlc,
                                     severity=csvFaultDict["Severity"],
                                     suffix=csvFaultDict["PV Suffix"],
                                     okValue=okCondition,
                                     faultValue=faultCondition,
                                     longDescription=csvFaultDict["Long Description"],
                                     shortDescription=csvFaultDict["Short Description"], prefix=prefix)

    def runThroughFaults(self):
        isOkay = True
        invalid = False

        for fault in self.faults.values():
            try:
                if fault.isFaulted():
                    isOkay = False
                    break
            except PvInvalid as e:
                print(e, " is disconnected")
                isOkay = False
                invalid = True
                break

        if isOkay:
            self.statusPV.put("{num}".format(num=str(self.number)))
            self.severityPV.put(0)
            self.descriptionPV.put(" ")
        else:
            self.statusPV.put(fault.tlc)
            self.descriptionPV.put(fault.shortDescription)
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
    key3 = displayHash(rack="", faultCondition="3", okCondition="", tlc="SSA")
    key2 = displayHash(rack="", faultCondition="2", okCondition="", tlc="SSA")

    ssaPVSuffix = "SSA:AlarmSummary.SEVR"

    leadingCavityH1 = h1.cavities[leader]
    leadingCavityH2 = h2.cavities[leader]

    h1.cavities[follower].faults[key3].pv = PV(leadingCavityH1.pvPrefix + ssaPVSuffix,
                                               connection_timeout=PV_TIMEOUT)
    h2.cavities[follower].faults[key3].pv = PV(leadingCavityH2.pvPrefix + ssaPVSuffix,
                                               connection_timeout=PV_TIMEOUT)
    h1.cavities[follower].faults[key2].pv = PV(leadingCavityH1.pvPrefix + ssaPVSuffix,
                                               connection_timeout=PV_TIMEOUT)
    h2.cavities[follower].faults[key2].pv = PV(leadingCavityH2.pvPrefix + ssaPVSuffix,
                                               connection_timeout=PV_TIMEOUT)

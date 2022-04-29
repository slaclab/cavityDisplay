from collections import OrderedDict

from epics import PV

from Fault import Fault, PvInvalid
from cavityDisplayGUI import SEVERITY_SUFFIX, STATUS_SUFFIX, DESCRIPTION_SUFFIX
from lcls_tools.devices.scLinac.scLinac import Cavity, SSA, make_lcls_cryomodules
from utils import CSV_FAULTS, displayHash


class DisplaySSA(SSA):
    def __init__(self, cavity):
        super().__init__(cavity)
        self.alarmSevrPV = PV(self.pvPrefix + "AlarmSummary.SEVR")


class DisplayCavity(Cavity):
    def __init__(self, cavityNum, rackObject, length=1.038, ssaClass=DisplaySSA):
        super(DisplayCavity, self).__init__(cavityNum, rackObject,
                                            length=length, ssaClass=ssaClass)
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


DISPLAY_CRYOMODULES = make_lcls_cryomodules(ssaClass=DisplaySSA,
                                            cavityClass=DisplayCavity)

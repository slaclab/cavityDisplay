from collections import OrderedDict

from epics import caput
from lcls_tools.superconducting.sc_linac import (
    Cavity,
    Cryomodule,
    Magnet,
    Piezo,
    Rack,
    SSA,
    StepperTuner,
    Machine,
)

from fault import Fault, PvInvalid
from utils import (
    CSV_FAULTS,
    DESCRIPTION_SUFFIX,
    SEVERITY_SUFFIX,
    STATUS_SUFFIX,
    display_hash,
)


class DisplaySSA(SSA):
    def __init__(self, cavity):
        super().__init__(cavity)
        self.alarmSevrPV: str = self.pv_addr("AlarmSummary.SEVR")


class SpreadsheetError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DisplayCryomodule(Cryomodule):
    def __init__(
        self,
        cryo_name,
        linac_object,
        cavity_class=Cavity,
        magnet_class=Magnet,
        rack_class=Rack,
        is_harmonic_linearizer=False,
        ssa_class=SSA,
        stepper_class=StepperTuner,
        piezo_class=Piezo,
    ):
        super().__init__(
            cryo_name=cryo_name,
            linac_object=linac_object,
        )
        for cavity in self.cavities.values():
            cavity.create_faults()

    @property
    def pydm_macros(self):
        """
        Currenlty only used for NIRP fault, but I think we can just keep adding
        to this list
        :return:
        """
        return "AREA={linac_name},CM={cm_name},RFNAME=CM{cm_name}".format(
            linac_name=self.linac.name, cm_name=self.name
        )


class DisplayCavity(Cavity):
    def __init__(
        self,
        cavity_num,
        rack_object,
    ):
        super(DisplayCavity, self).__init__(
            cavity_num=cavity_num, rack_object=rack_object
        )
        self.statusPV: str = self.pv_addr(STATUS_SUFFIX)
        self.severityPV: str = self.pv_addr(SEVERITY_SUFFIX)
        self.descriptionPV: str = self.pv_addr(DESCRIPTION_SUFFIX)

        self.faults: OrderedDict[int, Fault] = OrderedDict()

    def create_faults(self):
        for csvFaultDict in CSV_FAULTS:
            level = csvFaultDict["Level"]
            suffix = csvFaultDict["PV Suffix"]
            rack = csvFaultDict["Rack"]

            if level == "RACK":
                # Rack A cavities don't care about faults for Rack B and vice versa
                if rack != self.rack.rack_name:
                    # Takes us to the next iteration of the for loop
                    continue

                # tested in the python console that strings without one of these
                # formatting keys just ignores them and moves on
                prefix = csvFaultDict["PV Prefix"].format(
                    LINAC=self.linac.name,
                    CRYOMODULE=self.cryomodule.name,
                    RACK=self.rack.rack_name,
                    CAVITY=self.number,
                )
                pv = prefix + suffix

            elif level == "CRYO":
                prefix = csvFaultDict["PV Prefix"].format(
                    CRYOMODULE=self.cryomodule.name, CAVITY=self.number
                )
                pv = prefix + suffix

            elif level == "SSA":
                pv = self.ssa.pv_addr(suffix)

            elif level == "CAV":
                pv = self.pv_addr(suffix)

            elif level == "CM":
                cm_type = csvFaultDict["CM Type"]
                prefix = csvFaultDict["PV Prefix"].format(
                    LINAC=self.linac.name,
                    CRYOMODULE=self.cryomodule.name,
                    CAVITY=self.number,
                )

                if (cm_type == "1.3" and self.cryomodule.is_harmonic_linearizer) or (
                    cm_type == "3.9" and not self.cryomodule.is_harmonic_linearizer
                ):
                    continue
                pv = prefix + suffix

            elif level == "ALL":
                prefix = csvFaultDict["PV Prefix"]
                pv = prefix + suffix

            else:
                raise (SpreadsheetError("Unexpected fault level in fault spreadsheet"))

            tlc = csvFaultDict["Three Letter Code"]
            ok_condition = csvFaultDict["OK If Equal To"]
            fault_condition = csvFaultDict["Faulted If Equal To"]
            csv_prefix = csvFaultDict["PV Prefix"]

            key = display_hash(
                rack=rack,
                fault_condition=fault_condition,
                ok_condition=ok_condition,
                tlc=tlc,
                suffix=suffix,
                prefix=csv_prefix,
            )

            # setting key of faults dictionary to be row number b/c it's unique (i.e. not repeated)
            self.faults[key] = Fault(
                tlc=tlc,
                severity=csvFaultDict["Severity"],
                pv=pv,
                ok_value=ok_condition,
                fault_value=fault_condition,
                long_description=csvFaultDict["Long Description"],
                short_description=csvFaultDict["Short Description"],
                button_level=csvFaultDict["Button Type"],
                button_command=csvFaultDict["Button Path"],
                macros=self.edm_macro_string,
                button_text=csvFaultDict["Three Letter Code"],
                button_macro=csvFaultDict["Button Macros"],
                action=csvFaultDict["Recommended Corrective Actions"],
            )

    def run_through_faults(self):
        is_okay: bool = True
        invalid: bool = False

        for fault in self.faults.values():
            try:
                if fault.is_faulted():
                    is_okay = False
                    break
            except PvInvalid as e:
                print(e, " is disconnected")
                is_okay = False
                invalid = True
                break

        if is_okay:
            caput(self.statusPV, str(self.number))
            caput(self.severityPV, 0)
            caput(self.descriptionPV, " ")
        else:
            caput(self.statusPV, fault.tlc)
            caput(self.descriptionPV, fault.shortDescription)
            if not invalid:
                caput(self.severityPV, fault.severity)
            else:
                caput(self.severityPV, 3)


DISPLAY_MACHINE = Machine(
    ssa_class=DisplaySSA, cavity_class=DisplayCavity, cryomodule_class=DisplayCryomodule
)

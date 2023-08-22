from epics import PV

PV_TIMEOUT = 0.01


class PvInvalid(Exception):
    def __init__(self, message):
        super(PvInvalid, self).__init__(message)


class Fault:
    def __init__(
        self,
        tlc,
        severity,
        pv,
        ok_value,
        fault_value,
        long_description,
        short_description,
        button_level,
        button_command,
        macros,
        button_text,
        button_macro,
        action,
    ):
        self.tlc = tlc
        self.severity = int(severity)
        self.longDescription = long_description
        self.shortDescription = short_description
        self.okValue = float(ok_value) if ok_value else None
        self.faultValue = float(fault_value) if fault_value else None
        self.button_level = button_level
        self.button_command = button_command
        self.macros = macros
        self.button_text = button_text
        self.button_macro = button_macro
        self.action = action

        self.pv: PV = PV(pv, connection_timeout=PV_TIMEOUT)

    def is_faulted(self):
        """
        Dug through the pyepics source code to find the severity values:
        class AlarmSeverity(DefaultIntEnum):
            NO_ALARM = 0
            MINOR = 1
            MAJOR = 2
            INVALID = 3
        """
        if self.pv.severity == 3 or self.pv.status is None:
            raise PvInvalid(self.pv.pvname)

        if self.okValue is not None:
            return self.pv.value != self.okValue

        elif self.faultValue is not None:
            return self.pv.value == self.faultValue

        else:
            print(self)
            raise Exception(
                "Fault has neither 'Fault if equal to' nor"
                " 'OK if equal to' parameter"
            )

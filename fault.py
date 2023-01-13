from epics import PV

PV_TIMEOUT = 0.01


class PvInvalid(Exception):
    def __init__(self, message):
        super(PvInvalid, self).__init__(message)


class Fault:
    def __init__(self, tlc, severity, suffix, okValue, faultValue, longDescription,
                 shortDescription, prefix, button_level, button_command, macros,
                 button_text, button_macro):
        self.tlc = tlc
        self.severity = int(severity)
        self.longDescription = longDescription
        self.shortDescription = shortDescription
        self.okValue = float(okValue) if okValue else None
        self.faultValue = float(faultValue) if faultValue else None
        self.suffix = suffix
        self.button_level = button_level
        self.button_command = button_command
        self.macros = macros
        self.button_text = button_text
        self.button_macro = button_macro

        self.pv: PV = PV(prefix + suffix, connection_timeout=PV_TIMEOUT)

    def isFaulted(self):
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
            raise Exception("Fault has neither \'Fault if equal to\' nor"
                            " \'OK if equal to\' parameter")

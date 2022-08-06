from epics import caget

PV_TIMEOUT = 0.01


class PvInvalid(Exception):
    def __init__(self, message):
        super(PvInvalid, self).__init__(message)


class Fault:
    def __init__(self, tlc, severity, suffix, okValue, faultValue, longDescription,
                 shortDescription, prefix):
        self.tlc = tlc
        self.severity = int(severity)
        self.longDescription = longDescription
        self.shortDescription = shortDescription
        self.okValue = float(okValue) if okValue else None
        self.faultValue = float(faultValue) if faultValue else None
        self.suffix = suffix
        
        self.pv: str = (prefix + suffix)
    
    def isFaulted(self):
        print(f"Checking {self.pv}")
        
        """
        Dug through the pyepics source code to find the severity values:
        class AlarmSeverity(DefaultIntEnum):
            NO_ALARM = 0
            MINOR = 1
            MAJOR = 2
            INVALID = 3
        """
        if caget(self.pv + ".SEVR") == 3:
            raise PvInvalid(self.pv)
        
        if self.okValue is not None:
            return caget(self.pv) != self.okValue
        
        elif self.faultValue is not None:
            return caget(self.pv) == self.faultValue
        
        else:
            print(self)
            raise Exception("Fault has neither \'Fault if equal to\' nor"
                            " \'OK if equal to\' parameter")

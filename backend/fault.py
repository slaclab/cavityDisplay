from csv import DictReader
from epics import PV
from typing import Dict, List

PV_TIMEOUT = 0.01


class PvInvalid(Exception):
    def __init__(self, message):
        super(PvInvalid, self).__init__(message)


class Fault:
    def __init__(self, tlc, severity, suffix, okValue, faultValue, description,
                 name, prefix):
        self.tlc = tlc
        self.severity = int(severity)
        self.description = description
        self.name = name
        self.okValue = float(okValue) if okValue else None
        self.faultValue = float(faultValue) if faultValue else None

        self.pv: PV = PV(prefix + ":" + suffix, connection_timeout=PV_TIMEOUT)

    def __str__(self):
        return ', '.join("%s: %s" % item for item in vars(self).items())

    def isFaulted(self):
        if self.pv.status is None:
            raise PvInvalid(self.pv.pvname)

        if self.okValue is not None:
            return self.pv.value != self.okValue

        elif self.faultValue is not None:
            return self.pv.value == self.faultValue

        else:
            print(self)
            raise Exception("Fault has neither \'Fault if equal to\' nor"
                            " \'OK if equal to\' parameter")


csvFile = DictReader(open("faults.csv"))

CSV_FAULTS: List[Dict] = []
for row in csvFile:
    if row["PV Suffix"]:
        CSV_FAULTS.append(row)

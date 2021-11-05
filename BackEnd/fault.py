from csv import reader, DictReader
from epics import PV

import sys

sys.path.insert(0, '..')
from scLinac import LINACS, Cavity


class PvInvalid(Exception):
    def __init__(self, message):
        super(PvInvalid, self).__init__(message)


class Fault:
    def __init__(self, tlc, severity, rank, level, suffix, okValue, faultValue):
        self.tlc = tlc
        self.severity = int(severity)
        self.rank = rank
        self.level = level
        self.suffix = suffix
        self.okValue = float(okValue) if okValue else None
        self.faultValue = float(faultValue) if faultValue else None

    def __str__(self):
        return ', '.join("%s: %s" % item for item in vars(self).items())

    def __gt__(self, other):
        return self.rank > other.rank

    def isConnected(self, cavity):
        pass

    def isFaulted(self, faultPV):

        if faultPV.status is None:
            raise PvInvalid(faultPV)

        if self.okValue is not None:
            return faultPV.value != self.okValue

        elif self.faultValue is not None:
            return faultPV.value == self.faultValue

        else:
            print(self)
            raise Exception("Weird state, oh no")

    def writeToPVs(self):
        # if faulted, write tlc to CUDSTATUS pv and severity to CUDSEVR pv
        pass


faults = []
csvFile = DictReader(open("faults.csv"))
next(csvFile)
for row in csvFile:
    if row["PV Suffix"] and row["Level"] == "CAV":
        faults.append(Fault(row["Three Letter Code"], row["Severity"],
                            csvFile.line_num, row["Level"], row["PV Suffix"],
                            row["OK If Equal To"], row["Faulted If Equal To"]))

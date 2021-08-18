from csv import reader, DictReader
import pandas as pd


class Fault:
    def __init__(self, tlc, severity, rank):
        self.tlc = tlc
        self.severity = severity
        self.rank = rank
        print(tlc, severity, rank)

    def __gt__(self, other):
        return self.rank > other.rank

    def isFaulted(self):
        # This will come from columns D-G
        # aka Cav/rack/cm, PV, Ok value, fault value
        pass

    def writeToPVs(self):
        # if faulted, write tlc to CUDSTATUS pv and severity to CUDSEVR pv
        pass


csvFile = DictReader(open("faults.csv"))
for row in csvFile:
	fault = Fault(row["Three Letter Code"], row["Severity"], csvFile.line_num)





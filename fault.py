from csv import reader, DictReader
import pandas as pd
from scLinac import LINACS, Cavity
from epics import PV

class Fault:
    def __init__(self, tlc, severity, rank, level, suffix, okValue, faultValue):
        self.tlc = tlc
        self.severity = severity
        self.rank = rank
        self.level = level
        self.suffix = suffix
        self.okValue = okValue
        self.faultValue = faultValue

    def __gt__(self, other):
        return self.rank > other.rank

    def isFaulted(self, cavity=Cavity):
        # This will come from columns D-G
        # aka Cav/rack/cm, PV, Ok value, fault value
        pv = PV(cavity.pvPrefix + self.suffix)
        if self.okValue:
            return (pv.get() != self.okValue)
            
        elif self.faultValue:
            return (pv.get() == self.faultValue)
        
        else:
            raise("Weird state, oh no")

    def writeToPVs(self):
        # if faulted, write tlc to CUDSTATUS pv and severity to CUDSEVR pv
        pass

faults = []
csvFile = DictReader(open("faults.csv"))
csvFile.next()
for row in csvFile:
    if row["PV Suffix"] and row["Level"]=="CAV":
        faults.append(Fault(row["Three Letter Code"], row["Severity"], 
	                        csvFile.line_num, row["Level"], row["PV Suffix"],
	                        row["OK If Equal To"], row["Faulted If Equal To"]))





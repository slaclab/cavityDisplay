from csv import reader
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
'''
csvRowList = []
faults = []
csvReader = reader(open("faults.csv"))
header = next(csvReader)
print(header)

for row in csvReader:
    # print(row)
    csvRowList.append(row)
    #faults.append(Fault(row,csvReader.line_num))
'''

dataFrame = pd.read_csv('faults.csv')
pd.set_option('display.max_colwidth', -1)

for tlc, colorSeverity, rank in zip(dataFrame['TLC'][1:], dataFrame['Severity'][1:], dataFrame['Order'][1:]):
    Fault(tlc, colorSeverity, rank)






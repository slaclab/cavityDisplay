from csv import reader

class Fault:
    def __init__(self, rowData, rank):
        self.severity = int(rowData[8])
        self.rank = rank
        self.tlc = rowData[7]

    def __gt__(self, other):
        return self.rank > other.rank

    def isFaulted(self):
        # This will come from columns D-G
        # aka Cav/rack/cm, PV, Ok value, fault value
        pass

    def writeToPVs(self):
        # if faulted, write tlc to CUDSTATUS pv and severity to CUDSEVR pv
        pass

csvRowList = []
faults = []
csvReader = reader(open("faults.csv"))
header = next(csvReader)

for row in csvReader:
    print(row)
    csvRowList.append(row)
    faults.append(Fault(row,csvReader.line_num))


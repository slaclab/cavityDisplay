class Fault:
    def __init__(self, cavity, rowData):
        self.severity = rowData[3]
        self.tlc = rowData[4]
        self.pv = rowData[6].format(cavity.name, cavity.parent.name, cavity.grandparent.name)

    def __gt__(self, other):
        return self.severity > other.severity

    def isFaulted(self):
        pass

    def writeToPVs(self):
        pass

csvRowList = []
faults = []
reader = csvReader("faults.csv")
for row in reader:
    csvRowList.append(row)
    faults.append(Fault(row))


class Linac:
    def __init__(self, name, cryomodules):
        self.name = name
        self.cryomodules = []
        for cryomodule in cryomodules:
            self.cryomodules.append(Cryomodule(cryomodule, self))

class Cryomodule:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.cavities = []
        for i in range(1, 9):
            self.cavities.append(Cavity(i, self))

class Cavity:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.grandparent = self.parent.parent


linacs = [Linac("L0B", ["01"]),
          Linac("L1B", ["02", "03", "H1", "H2"]),
          Linac("L2B", ["04", "05", "06", "07", "08", "09", "10", "11", "12",
                        "13", "14", "15"]),
          Linac("L3B", ["16", "17", "18", "19", "20", "21", "22", "23", "24",
                        "25", "26", "27", "28", "29", "30", "31", "32", "33",
                        "34", "35"])]


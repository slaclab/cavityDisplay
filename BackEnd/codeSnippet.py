from csv import DictReader
from epics import PV

DESCRIPTION_SUFFIX = "CUDDESC"


# Read in tlc, severity, and pv name from fault spreadsheet
csvFile = DictReader(open("faults.csv"))

CSV_FAULTS = []
for row in csvFile:
    if row["PV Suffix"]:
        CSV_FAULTS.append(row)

faults = []
for csvFault in CSV_FAULTS:
    faults.append(csvFault["Name"])



example_pvPrefix = "ACCL:L2B:0920:"
namePV = PV(example_pvPrefix + DESCRIPTION_SUFFIX)

# Arbitrarily picking index 0 which should be "Parked"
print(faults[0])
namePV.put(faults[0])
print(namePV.get())


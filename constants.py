from csv import DictReader
from typing import Dict, List

CSV_FAULTS: List[Dict] = []
for row in DictReader(open("faults.csv")):
    if row["PV Suffix"]:
        CSV_FAULTS.append(row)

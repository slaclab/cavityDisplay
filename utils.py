from csv import DictReader
from typing import Dict, List

DEBUG = False
BACKEND_SLEEP_TIME = 10

CSV_FAULTS: List[Dict] = []
for row in DictReader(open("faults.csv")):
    if row["PV Suffix"]:
        CSV_FAULTS.append(row)


def displayHash(rack: str, faultCondition: str, okCondition: str, tlc: str):
    return hash(rack) ^ hash(faultCondition) ^ hash(okCondition) ^ hash(tlc)

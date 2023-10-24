from csv import DictReader

from typing import Dict, List

STATUS_SUFFIX = "CUDSTATUS"
SEVERITY_SUFFIX = "CUDSEVR"
DESCRIPTION_SUFFIX = "CUDDESC"
RF_STATUS_SUFFIX = "RFSTATE"

DEBUG = False
BACKEND_SLEEP_TIME = 10

CSV_FAULTS: List[Dict] = []
for row in DictReader(open("faults.csv", encoding='utf-8-sig')):
    if row["PV Suffix"]:
        CSV_FAULTS.append(row)


def displayHash(rack: str, faultCondition: str, okCondition: str, tlc: str, suffix: str,
                prefix: str):
    return hash(rack) ^ hash(faultCondition) ^ hash(okCondition) ^ hash(tlc) ^ hash(suffix) ^ hash(prefix)

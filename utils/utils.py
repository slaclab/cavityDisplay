from csv import DictReader

from typing import Dict, List

DEBUG = True
BACKEND_SLEEP_TIME = 10

STATUS_SUFFIX = "CUDSTATUS"
SEVERITY_SUFFIX = "CUDSEVR"
DESCRIPTION_SUFFIX = "CUDDESC"
RF_STATUS_SUFFIX = "RFSTATE"


def parse_csv() -> List[Dict]:
    faults: List[Dict] = []
    for row in DictReader(open("utils/faults.csv", encoding="utf-8-sig")):
        if row["PV Suffix"]:
            faults.append(row)
    return faults


def display_hash(
    rack: str,
    fault_condition: str,
    ok_condition: str,
    tlc: str,
    suffix: str,
    prefix: str,
):
    return (
        hash(rack)
        ^ hash(fault_condition)
        ^ hash(ok_condition)
        ^ hash(tlc)
        ^ hash(suffix)
        ^ hash(prefix)
    )


class SpreadsheetError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

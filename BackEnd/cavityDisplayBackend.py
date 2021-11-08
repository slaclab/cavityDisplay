from backEnd_constants import DISPLAY_LINACS
from epics import caput_many


class DisplayValues:
    def __init__(self):
        self.statusNames = []
        self.statusValues = []
        self.severityNames = []
        self.severityValues = []

    def clearLists(self):
        self.statusNames = []
        self.statusValues = []
        self.severityNames = []
        self.severityValues = []


displayValues = DisplayValues()

while True:
    for linac in DISPLAY_LINACS:
        for cryomodule in linac.cryomodules.values():
            for cavity in cryomodule.cavities.values():
                cavity.runThroughFaults(displayValues)

    caput_many(displayValues.statusNames + displayValues.severityNames,
               displayValues.statusValues + displayValues.severityValues)
    displayValues.clearLists()

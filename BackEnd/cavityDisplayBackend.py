from backEnd_constants import DISPLAY_LINACS
from epics import caput_many
from time import time


class DisplayValues:
    def __init__(self):
        self.statusNames = []
        self.statusValues = []
        self.severityNames = []
        self.severityValues = []

    def clearLists(self):
        self.statusNames*=0
        self.statusValues*=0
        self.severityNames*=0
        self.severityValues*=0
        

displayValues = DisplayValues()


try:
    while True:
        start = time()
        for linac in DISPLAY_LINACS:
            for cryomodule in linac.cryomodules.values():
                for cavity in cryomodule.cavities.values():
                    cavity.runThroughFaults(displayValues)

        caput_many(displayValues.statusNames + displayValues.severityNames,
                displayValues.statusValues + displayValues.severityValues)

        displayValues.clearLists()

        print(time() - start)
        
except KeyboardInterrupt:
    print('Interuption! Program will end within the next minute (aka please be patient)')
    pass
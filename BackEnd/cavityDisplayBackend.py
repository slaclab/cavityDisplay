from fault import *
from backEnd_constants import STATUS_SUFFIX, SEVERITY_SUFFIX, DISPLAY_LINACS
from epics import PV, caput_many
from time import time

import sys
sys.path.insert(0, '..')
from scLinac import LINACS, Cavity, Linac


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
    start = time()
    for linac in DISPLAY_LINACS:
        for _, cryomodule in linac.cryomodules.items():
            for _, cavity in cryomodule.cavities.items():
                cavity.runThroughFaults(displayValues)

    caput_many(displayValues.statusNames + displayValues.severityNames,
               displayValues.statusValues + displayValues.severityValues)
    #caput_many(displayValues.severityNames, displayValues.severityValues)
    displayValues.clearLists()
    
    print(time()-start)



from fault import *
from scLinac import LINACS, Cavity, Linac
from constants import STATUS_SUFFIX, SEVERITY_SUFFIX, DISPLAY_LINACS
from epics import PV, caput_many
from time import time

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
        print(linac.name)
        for _, cryomodule in linac.cryomodules.items():
            print(cryomodule.name)
            for _, cavity in cryomodule.cavities.items():
                print(cavity.number)
                cavity.runThroughFaults(displayValues)
    caput_many(displayValues.statusNames, displayValues.statusValues)
    caput_many(displayValues.severityNames, displayValues.severityValues)
    displayValues.clearLists()
    
    print(time()-start)



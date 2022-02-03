from backEnd_constants import DISPLAY_LINACS
from time import time


while True:
    start = time()
    for linac in DISPLAY_LINACS:
        for cryomodule in linac.cryomodules.values():
            for cavity in cryomodule.cavities.values():
                cavity.runThroughFaults()

    print(time() - start)

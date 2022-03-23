from time import time

from displayCavity import DISPLAY_LINAC_OBJECTS

while True:
    start = time()
    for linac in DISPLAY_LINAC_OBJECTS:
        for cryomodule in linac.cryomodules.values():
            for cavity in cryomodule.cavities.values():
                cavity.runThroughFaults()

    print(time() - start)

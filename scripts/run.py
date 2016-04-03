import os
import time
from extractEpicNo import *

i = 1
for number in epicNumbers:
    os.system('python extractData.py' + ' ' + number + ' ' + str(i))
    time.sleep(0.5)
    i = i + 1

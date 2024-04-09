

import random
import subprocess

from glob import glob

masker_files = (glob('olkisa_masker/*.wav'))

count: int = 0
max_count: int = 5

while count < max_count:
    for i in range(len(masker_files)):
        random_masker = (random.choice(masker_files))
        return_code = subprocess.call(["afplay", random_masker])
        break
    count = count + 1
    if count == max_count:
        print('Test zu Ende')


# change
import random
import subprocess
from glob import glob
from pathlib import Path
import slab

def select_random_speech(target_path=Path.cwd() / 'olkisa_targets',
                         masker_path=Path.cwd() / 'olkisa_masker', n_trials=30):
    masker_files = list(masker_path.glob('*.wav'))
    target_files = list(target_path.glob('*.wav'))

    masker_l_wavs = []
    masker_r_wavs = []
    target_wavs = []
    wav_list = []

    while n_trials <= 30:
        for i in range(n_trials):
            print(i)
            random_masker_path = (random.choice(masker_files))
            random_masker_wav = slab.Sound(random_masker_path)
            masker_wavs.append(random_masker_wav)
        for i in range(n_trials):
            print(i)
            random_target_path = (random.choice(target_files))
            random_target_wav = slab.Sound(random_target_path)
            target_wavs.append(random_target_wav)


        # todo do this with target sounds

    return target_wavs, masker_l_wavs, masker_r_wavs

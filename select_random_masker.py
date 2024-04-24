import random
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import subprocess
from glob import glob
from pathlib import Path
import numpy
import slab

def select_random_speech(wav_path=Path.cwd() / 'wav_data', n_trials=30):

    numbered_folders = list(wav_path.glob('*'))

    for trial in range(n_trials):
        random_numbered_folders = numpy.random.choice(numbered_folders, size=5, replace=False)
        wav_list = []
        for folder in random_numbered_folders:
            numbered_wavs = list(folder.glob('*.wav'))
            random_wav = numpy.random.choice(numbered_wavs)
            random_wav = slab.Sound(random_wav)
            wav_list.append(random_wav)
        sound1 = wav_list[0]
        sound2 = wav_list[1]

        sound1.waveform()


        data1 = sound1.data
        data2 = sound2.data
        max_len = numpy.max([len(data1), len(data2)])
        numpy.pad(data1, (0, numpy.diff(len(data1), len(data2))))
        # todo make sure they have the same length
        merged = sound1 + sound2

        merged_sound = slab.Sound(data=merged)



        # todo


    return target_wavs, masker_l_wavs, masker_r_wavs

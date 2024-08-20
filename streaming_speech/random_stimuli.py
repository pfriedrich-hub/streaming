import copy
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from pathlib import Path
import numpy
import slab


def select_random_speech(n_trials=30, level=85, wav_path=Path.cwd() / 'data' / 'wav_data'):

    numbered_folders = list(wav_path.glob('*'))
    masker_l_list = []  # list containing n_trials stimuli#
    masker_r_list = []  # list containing n_trials stimuli
    target_list = []  # list containing n_trials stimuli
    random_numbered_folders = []

    for trial in range(n_trials):
        random_numbered_folders.append(list(numpy.random.choice(numbered_folders, size=5, replace=False)))

    for idx in range(n_trials-2):
        while (random_numbered_folders[idx+1][4] == random_numbered_folders[idx][4] or
                random_numbered_folders[idx+1][4] == random_numbered_folders[idx+2][4]):
            random_numbered_folders[idx + 1][4] = numpy.random.choice(numbered_folders, size=1, replace=False)[0]
            while random_numbered_folders[idx + 1][4] in random_numbered_folders[idx + 1][:4]:
                random_numbered_folders[idx + 1][4] = numpy.random.choice(numbered_folders, size=1, replace=False)[0]

    for trial in range(n_trials):
        random_numbered_folders_trial = random_numbered_folders[trial]
        speech_list = []
        n_samples = []
        wav_path_list = []  # just to test
        for folder in random_numbered_folders_trial:
            numbered_wavs = list(folder.glob('*.wav'))
            wav = numpy.random.choice(numbered_wavs)
            wav_path_list.append(wav)
            speech = slab.Sound(wav)
            speech.level = level
            n_samples.append(speech.n_samples)
            speech_list.append(speech)

        # # choose the two shortest sentences and mix them with the two longest sentences
        # shortest_idx = numpy.argpartition(n_samples, 2)[:2]
        # longest_idx = numpy.argpartition(n_samples, len(n_samples) - 2)[-2:]
        # delay = 200  # delay for one of the sounds to mix in ms
        # delay_n_samples = 200 * 50   # delay in samples

        for speech in speech_list:
            pad_len = numpy.diff((speech.n_samples, numpy.max(n_samples)))[0]
            data = numpy.pad(speech.data[:, 0], (0, pad_len))
            speech.data = numpy.expand_dims(data, axis=1)

        masker_l_list.append(speech_list[0] + speech_list[1])  # list containing n_trials stimuli#
        masker_r_list.append(speech_list[2] + speech_list[3]) # list containing n_trials stimuli
        target_list.append(speech_list[4])  # list containing n_trials stimuli

    return target_list, masker_l_list, masker_r_list

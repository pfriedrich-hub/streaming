import matplotlib
matplotlib.use('TkAgg')
import numpy
import freefield
import time
from pathlib import Path
data_path = Path.cwd() / 'data'


def noise_streaming():
    # liste der zu initialisierenden prozessoren und dazugehörige rcx files
    proc_list = [['RX81', 'RX8', data_path / 'rcx' / 'streaming_noise.rcx'],
                 ['RX82', 'RX8', data_path / 'rcx' / 'streaming_speech.rcx'],
                ['RP2', 'RP2', data_path / 'rcx' / '4_buttons.rcx']]
    # initialize processors
    freefield.initialize(setup='dome', device=proc_list)
    freefield.load_equalization(data_path / 'calibration' / 'calibration_dome_01.03.pkl')
    freefield.set_logger('warning')
    # set experiment parameters
    target_speaker_id = 23
    isi = 100  # time between stimuli (inter stim interval)
    stim_duration = 150  # stim duration
    soa = isi + stim_duration  # time between onsets (stim onset async)
    stim_duration_samples = stim_duration * 50

    # generate target amplitudes
    target_amp = 85
    non_target_amp = 45
    n_targets = 10
    n_stim = 50
    n_list = int(n_stim / n_targets)  # mittlere abstand zwischen zwei targets
    target_amp_list = []
    for i in range(n_targets):
        list = [non_target_amp] * n_list
        rnd_idx = numpy.random.randint(2, n_list - 2)  # leave the first and last places free
        list[rnd_idx] = target_amp
        target_amp_list.extend(list)

    # write general parameters
    freefield.write(tag='soa', value=soa, processors=['RX81'])
    freefield.write(tag='stim_duration', value=stim_duration_samples, processors=['RX81'])

    # write target parameters
    freefield.write(tag='target_n_trials', value=len(target_amp_list), processors=['RX81'])
    freefield.write(tag='target_amps', value=target_amp_list, processors=['RX81'])
    freefield.write(tag='target_channel', value=target_speaker_id, processors=['RX81'])

    freefield.play()
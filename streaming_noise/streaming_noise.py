import matplotlib
matplotlib.use('TkAgg')
import numpy
import freefield
import time
from pathlib import Path
data_path = Path.cwd() / 'data'
from matplotlib import pyplot as plt

def noise_streaming():
    # liste der zu initialisierenden prozessoren und dazugehörige rcx files
    proc_list = [['RX81', 'RX8', data_path / 'rcx' / 'streaming_noise.rcx'],
                 ['RX82', 'RX8', data_path / 'rcx' / 'streaming_speech.rcx'],
                ['RP2', 'RP2', data_path / 'rcx' / '4_buttons.rcx']]
    # initialize processors
    freefield.initialize(setup='dome', device=proc_list)
    freefield.load_equalization(data_path / 'calibration' / 'calibration_dome_01.03.pkl')
    freefield.set_logger('info')

    # set experiment parameters
    # loudspeakers
    masker_l_az = -52.5
    masker_r_az = 52.5
    masker_l_speaker_id = (masker_l_az, 0)
    masker_r_speaker_id = (masker_r_az, 0)
    target_speaker_id = (0, 0)

    # stim numbers
    n_stim = 320
    n_targets = 20

    # timing parameters
    isi = 50  # time between stimuli (inter stim interval)
    stim_duration = 50  # stim duration
    soa = isi + stim_duration  # time between onsets (stim onset async)
    stim_duration_samples = stim_duration * 50
    masker_l_delay = 25
    masker_r_delay = 15

    # amplitudes
    baseline_amp = 65
    amp_range = 30

    ceiling_amp = baseline_amp + amp_range
    target_amp = baseline_amp + amp_range / 3
    non_target_amp = ceiling_amp - amp_range / 3
    masker_amps = [baseline_amp + amp_range / 5, baseline_amp + amp_range / 2.5,
                   ceiling_amp - amp_range / 2.5, ceiling_amp - amp_range / 5]

    # randomize amps
    # target amps
    n_list = int(n_stim / n_targets)  # mittlere abstand zwischen zwei targets
    target_amp_list = []
    for i in range(n_targets):
        list = [non_target_amp] * n_list
        rnd_idx = numpy.random.randint(4, n_list - 4)  # leave the first and last places free
        list[rnd_idx] = target_amp
        # print(list)
        target_amp_list.extend(list)

    # generate masker amplitudes
    masker_l_amps = [60, 65, 70, 75]
    masker_l_amp_list = []
    for i in range(n_stim):
        masker_l_amp_list.extend(numpy.random.choice(masker_amps, 4, replace=False).tolist())

    masker_r_amps = [60, 65, 70, 75]
    masker_r_amp_list = []
    for i in range(n_stim):
        masker_r_amp_list.extend(numpy.random.choice(masker_amps, 4, replace=False).tolist())


    # write general parameters
    freefield.write(tag='soa', value=soa, processors=['RX81', 'RX82'])
    freefield.write(tag='stim_duration', value=stim_duration_samples, processors=['RX81'])
    freefield.write(tag='n_stim', value=n_stim, processors=['RX81'])

    # write target parameters
    freefield.write(tag='target_amps', value=target_amp_list, processors=['RX81'])
    freefield.write(tag='target_channel', value=freefield.pick_speakers(target_speaker_id)[0].analog_channel,
                    processors=['RX81'])

    # write masker parameters
    # left
    freefield.write(tag='masker_l_amps', value=masker_l_amp_list, processors=['RX81'])
    freefield.write(tag='masker_l_channel', value=freefield.pick_speakers(masker_l_speaker_id)[0].analog_channel,
                    processors=['RX81'])
    freefield.write(tag='masker_l_delay', value=masker_l_delay, processors=['RX81'])

    # right
    freefield.write(tag='masker_r_amps', value=masker_r_amp_list, processors=['RX82'])
    freefield.write(tag='masker_r_channel', value=freefield.pick_speakers(masker_r_speaker_id)[0].analog_channel,
                    processors=['RX82'])
    freefield.write(tag='masker_r_delay', value=masker_r_delay, processors=['RX82'])
    freefield.play()
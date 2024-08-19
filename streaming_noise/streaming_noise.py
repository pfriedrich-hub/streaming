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
                 ['RX82', 'RX8', data_path / 'rcx' / 'streaming_noise.rcx'],
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

    # stim numbers in target stream
    n_stim = 320
    n_targets = 20

    # timing parameters
    soa = 550  # time between onsets (stim onset async)

    # amplitudes
    baseline_amp = 30
    amp_range = 65
    ceiling_amp = baseline_amp + amp_range
    masker_amps = [baseline_amp + amp_range / 5, baseline_amp + amp_range / 2.5,
                   ceiling_amp - amp_range / 2.5, ceiling_amp - amp_range / 5]
    target_amp = masker_amps[3]
    non_target_amp = masker_amps[1]

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
    masker_l_amp_list = []
    for i in range(int(n_stim/4)):
        masker_l_amp_list.extend(numpy.random.choice(masker_amps, 4, replace=False).tolist())
    masker_r_amp_list = []
    for i in range(int(n_stim/4)):
        masker_r_amp_list.extend(numpy.random.choice(masker_amps, 4, replace=False).tolist())

    # write general parameters
    freefield.write(tag='soa', value=soa, processors=['RX81', 'RX82'])
    freefield.write(tag='n_stim', value=n_stim, processors=['RX81', 'RX82'])
    freefield.write(tag='target_amp', value=target_amp, processors=['RX81', 'RX82'])

    # write target parameters
    freefield.write(tag='target_amps', value=target_amp_list, processors=['RX81', 'RX82'])
    freefield.write(tag='target_channel', value=freefield.pick_speakers(target_speaker_id)[0].analog_channel,
                    processors=freefield.pick_speakers(target_speaker_id)[0].analog_proc)

    # write masker parameters
    # left
    # freefield.write(tag='masker_l_amps', value=masker_l_amp_list,
    #                 processors=freefield.pick_speakers(masker_l_speaker_id)[0].analog_proc)
    # freefield.write(tag='masker_l_channel', value=freefield.pick_speakers(masker_l_speaker_id)[0].analog_channel,
    #                 processors=freefield.pick_speakers(masker_l_speaker_id)[0].analog_proc)
    #
    # # right
    # freefield.write(tag='masker_r_amps', value=masker_r_amp_list,
    #                 processors=freefield.pick_speakers(masker_r_speaker_id)[0].analog_proc)
    # freefield.write(tag='masker_r_channel', value=freefield.pick_speakers(masker_r_speaker_id)[0].analog_channel,
    #                 processors=freefield.pick_speakers(masker_r_speaker_id)[0].analog_proc)

    # get subject responses
    freefield.play()

    running = True

    n_hits = freefield.read('n_hits', 'RX82')
    c_targets = freefield.read('n_targets', 'RX82')
    n_buttons = freefield.read('n_buttons', 'RX82')
    while running:
        c_hits = freefield.read('n_hits', 'RX82')
        if c_hits > n_hits:
            n_hits = c_hits
            # level up

        c_targets = freefield.read('n_targets', 'RX82')
        if c_targets > n_targets:
            n_targets = c_targets
            # check if c_hits > n_hits (hits increase) over the next 300-700 ms:
                # level down

        n_targets = freefield.read('n_targets', 'RX82')
        n_buttons = freefield.read('n_buttons', 'RX82')

    if
         # level up



    playing = True
    #
    # while not button =
    #     freefield.play('B')
    # time.sleep() # todo wait for experiment to finish (loop through blocks)
    # freefield.halt()

if __name__ == "__main__":
    noise_streaming()

#todo implement bp filter


    # data = freefield.read(tag='data',
    #                 processor='RX81', n_samples=2000)
import matplotlib
matplotlib.use('TkAgg')
import numpy
import freefield
import time
from pathlib import Path
data_path = Path.cwd() / 'data'
from matplotlib import pyplot as plt
from pynput.keyboard import Controller
keyboard = Controller()
# import game.python_for_jar as python_for_jar

def noise_streaming(masker_on=True):

    # set experiment parameters
    # loudspeakers
    if masker_on:
        azimuths = [52.5, 35, 17.5]
    else:
        azimuths = [52.5]

    for azimuth in azimuths:
        masker_l_az = -azimuth
        masker_r_az = azimuth
        masker_l_speaker_id = (masker_l_az, 0)
        masker_r_speaker_id = (masker_r_az, 0)
        target_speaker_id = (0, 0)

        if masker_on:
            # stim numbers in target stream
            n_stim = 160
            n_targets = 18
        else:
            n_stim = 100
            n_targets = 12

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
            rnd_idx = numpy.random.randint(numpy.round(n_list / 4), n_list - numpy.round(n_list / 4))  # leave the first and last places free
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

        # reset masker channels before reassigning them to a new condition
        freefield.write(tag='masker_l_channel', value=99, processors=['RX81', 'RX82'])
        freefield.write(tag='masker_r_channel', value=99, processors=['RX81', 'RX82'])

        if masker_on:
            # write masker parameters
            # left
            freefield.write(tag='masker_l_amps', value=masker_l_amp_list,
                            processors=['RX81', 'RX82'])
            freefield.write(tag='masker_l_channel', value=freefield.pick_speakers(masker_l_speaker_id)[0].analog_channel,
                            processors=freefield.pick_speakers(masker_l_speaker_id)[0].analog_proc)
            # right
            freefield.write(tag='masker_r_amps', value=masker_r_amp_list,
                            processors=['RX81', 'RX82'])
            freefield.write(tag='masker_r_channel', value=freefield.pick_speakers(masker_r_speaker_id)[0].analog_channel,
                            processors=freefield.pick_speakers(masker_r_speaker_id)[0].analog_proc)

        input(f'Next condition {(-azimuth, azimuth)} Press button to start.')
        freefield.wait_for_button('RX82', 'button')

        start_time = time.time()
        freefield.play()
        n_hits = 0
        n_missed = 0
        n_false_positives = 0
        while start_time + (n_stim * soa / 1000) > time.time():
            time.sleep(0.1)
            hits = freefield.read('n_hits', 'RX82')
            missed = freefield.read('n_missed', 'RX82')
            false_positives = freefield.read('n_fp', 'RX82')
            if hits == n_hits + 1:
                press('+')
                print('hit')
                n_hits = hits
            if missed == n_missed + 1:
                press('-')
                print('miss')
                n_missed = missed
            if false_positives == n_false_positives + 1:
                press('-')
                print('fp')
                n_false_positives = false_positives     # todo check fp

                # todo write to excel

def press(key):
    keyboard.press(key)
    keyboard.release(key)

if __name__ == "__main__":
    # initialize processors
    proc_list = [['RX81', 'RX8', data_path / 'rcx' / 'streaming_noise.rcx'],
                 ['RX82', 'RX8', data_path / 'rcx' / 'streaming_noise.rcx'],
                 ['RP2', 'RP2', data_path / 'rcx' / '4_buttons.rcx']]
    freefield.initialize(setup='dome', device=proc_list)
    freefield.set_logger('info')
    noise_streaming(masker_on=False)
    # noise_streaming(masker_on=True)
    freefield.halt()
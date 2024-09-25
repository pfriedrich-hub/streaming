import matplotlib
matplotlib.use('TkAgg')
import numpy
import freefield
import time
from pathlib import Path
data_path = Path.cwd() / 'data'
from matplotlib import pyplot as plt
from pynput.keyboard import Controller
from write_results import *
keyboard = Controller()
# import game.python_for_jar as python_for_jar

# todo first connect single button to RX82
# todo before starting the experiment:
#  1. extend display to the lab screen
#  2. open and run game/python_for_jar.py and move window to lab screen
#  3. enter subject id
#  4. start experiment: right click + 'run' (click game window tab, close excel file)
#  press button to start

# this is the subject id that will be saved in an excel sheet (together with behavior data)
subject_id = 'test1'

def noise_streaming(masker_on=True):

    # set experiment parameters
    # loudspeakers
    if masker_on:
        azimuths = [52.5, 35, 17.5]
    else:
        azimuths = [52.5]

    # butterworth filter settings
    freefield.write('FC', 2075.0, ['RX81', 'RX82'])
    freefield.write('BW', 3750.0, ['RX81', 'RX82'])
    write_subject(subject_id)  # write subject id to new row

    for azimuth in azimuths:
        masker_l_speaker_id = (-azimuth, 0)
        masker_r_speaker_id = (azimuth, 0)
        target_speaker_id = (0, 0)

        if masker_on:
            # stim numbers in target stream
            n_stim = 160
            n_targets = 18
        else:
            n_stim = 75
            n_targets = 15

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

        # reduce masker amps
        masker_amps = [masker_amp - 30 for masker_amp in masker_amps]

        # randomize amps
        # target amps
        n_list = int(n_stim / n_targets)  # mittlere abstand zwischen zwei targets
        target_amp_list = []
        while len(target_amp_list) < n_stim:
            list = [non_target_amp] * n_list
            rnd_idx = numpy.random.randint(numpy.round(n_list / 4), n_list - numpy.round(n_list / 4))  # leave the first and last places free
            list[rnd_idx] = target_amp
            # print(list)
            target_amp_list.extend(list)
        target_amp_list = target_amp_list[:n_stim]

        if not masker_on:  # remove targets from the first 20 stimuli
            target_amp_list[:20] = [non_target_amp]*20

        # generate masker amplitudes
        masker_l_amp_list = []
        masker_r_amp_list = []
        for i in range(int(n_stim/4)):
            masker_l_amp_list.extend(numpy.random.choice(masker_amps, 4, replace=False).tolist())
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

        [led_speaker] = freefield.pick_speakers(23)  # get object for center speaker LED
        freefield.write(tag='bitmask', value=led_speaker.digital_channel,
              processors=led_speaker.digital_proc)  # illuminate LED
        freefield.wait_for_button('RX82', 'start_button')
        freefield.write(tag='bitmask', value=0, processors=led_speaker.digital_proc)  # illuminate LED

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
                n_false_positives = false_positives

        if masker_on:
            write_to_xls(subject_id, condition=azimuth, hits=n_hits, missed=n_missed, false_positive=n_false_positives)

def press(key):
    keyboard.press(key)
    keyboard.release(key)

if __name__ == "__main__":
    # initialize processors
    proc_list = [['RX81', 'RX8', data_path / 'rcx' / 'streaming_noise_RX81.rcx'],
                 ['RX82', 'RX8', data_path / 'rcx' / 'streaming_noise_RX82.rcx']]
    freefield.initialize(setup='dome', device=proc_list)
    freefield.set_logger('debug')
    noise_streaming(masker_on=False)
    noise_streaming(masker_on=True)
    freefield.halt()
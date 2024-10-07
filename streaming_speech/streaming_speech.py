import matplotlib
matplotlib.use('TkAgg')
import freefield
import time
from pathlib import Path

from random_stimuli import select_random_speech
#from streaming_speech.random_stimuli import select_random_speech   # Aufruf am 7.10. wurde nicht akzeptiert

from gui_streaming_speech_3_conditions import *
#import streaming_speech.gui_streaming_speech_3_conditions as gui   # Aufruf am 7.10. wurde nicht akzeptiert

samplerate = 48828
data_path = Path.cwd() / 'data'
results_file = Path.cwd() / 'results' / 'gui_get_results_streaming_speech.xlsx'
conditions = ['52.5°', '35°', '17.5°']

n_trials = 6

# todo first connect button to RP2
# todo first to start experiment press str + A and f9

# todo calibrate SNR - test this
# todo format gui for desktop in lab 1600 x 1200

def speech_streaming():
    # liste der zu initialisierenden prozessoren und dazugehörige rcx files
    proc_list = [['RX81', 'RX8', data_path / 'rcx' / 'streaming_speech.rcx'],
                 ['RX82', 'RX8', data_path / 'rcx' / 'streaming_speech.rcx'],
                ['RP2', 'RP2', data_path / 'rcx' / '4_buttons.rcx']]
    # initialize processors
    freefield.initialize(setup='dome', device=proc_list)
    freefield.set_logger('warning')
    # set experiment parameters
    n_blocks = 3
    target_level = 85  # level in dB
    masker_level = 75
    # set initial speakers
    azimuths = [52.5, 35, 17.5]
    target_speaker_id = (0, 0)

    # open gui
    window = gui.open_gui(results_file)  # create window wait for start button

    # iterate over blocks
    for block in range(n_blocks):

        # set masker speakers for each block
        masker_l_speaker_id = (azimuths[block], 0)
        masker_r_speaker_id = (-azimuths[block], 0)

        response = None
        print('Press button 4 to start the next block.')
        while not response == 4:  # wait for button no 4 to start block
            response = freefield.read('button', 'RP2')
            time.sleep(0.1)

        # get stimuli for each block
        target_list, masker_l_list, masker_r_list = select_random_speech(n_trials=n_trials, target_level=target_level,
                                                masker_level=masker_level, wav_path=Path.cwd() / 'data' / 'wav_data')
        # iterate over trials
        responses = []
        for trial_idx in range(n_trials):
            # print(trial_idx)
            # write target sound and speaker to corresponding processor
            freefield.set_signal_and_speaker(signal=target_list[trial_idx], speaker=target_speaker_id, equalize=False, data_tag='data_target',
                                   chan_tag='target_ch', n_samples_tag='n_target')

            freefield.set_signal_and_speaker(signal=masker_l_list[trial_idx], speaker=masker_l_speaker_id, equalize=False, data_tag='data_masker_l',
                                   chan_tag='masker_l_ch', n_samples_tag='n_masker_l')

            freefield.set_signal_and_speaker(signal=masker_r_list[trial_idx], speaker=masker_r_speaker_id, equalize=False, data_tag='data_masker_r',
                                   chan_tag='masker_r_ch', n_samples_tag='n_masker_r')
            # send trigger to play the sound
            time.sleep(1)
            freefield.play()
            freefield.wait_to_finish_playing()
            print(f'Target sentence: {Path(target_list[trial_idx].name).name}')
            print('Bitte gib die Anzahl der gehörten Wörter ein.')
            response = None
            while not response:  # wait for and read button
                response = freefield.read('button', 'RP2')
                time.sleep(0.1)
            responses.append(response)
            print(f'{int(response)} Wörter erkannt')

        # count button responses
        b1 = responses.count(1)
        b2 = responses.count(2)
        b3 = responses.count(3)
        b4 = responses.count(4)
        responses = [b1, b2, b3, b4]
        gui.add_responses(window, conditions[block], responses)

if __name__ == "__main__":
    speech_streaming()
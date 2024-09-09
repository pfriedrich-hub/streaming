import matplotlib
matplotlib.use('TkAgg')
import freefield
import time
from pathlib import Path
from streaming_speech.random_stimuli import select_random_speech
import streaming_speech.gui_streaming_speech_3_conditions as gui

samplerate = 48828
data_path = Path.cwd() / 'data'
results_file = Path.cwd() / 'results' / 'gui_get_results_streaming_speech.xlsx'
conditions = ['52.5°', '35°', '17.5°']

n_trials = 6

# todo connect tablet and show current target sentence
#  calibrate SNR - test this

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
    window = gui.open_gui(results_file)  # create winod and wait for start button

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


"""import time
from pathlib import Path
import random
import freefield
import slab


def play(s,azi=0,f='0.wav'):
# DELETE ON FREEFIELD PC!!
    import subprocess
    s = slab.Binaural(s)
    itd = slab.Binaural.azimuth_to_itd(azi)
    s = s.itd(itd)
    s.write(f)
    subprocess.call(['afplay '+f+' &'], shell=True)

# def reverse(masker_sentences):  # do not reverse
#     for i,_ in enumerate(masker_sentences):
#         masker_sentences[i].data = masker_sentences[i].data[::-1,:].copy() # copy not needed in production!

def mix(masker_sentences):  # 
    if masker_sentences[0].n_samples > masker_sentences[1].n_samples:
        m1 = masker_sentences[1].resize(masker_sentences[0].n_samples)
        masker_left = masker_sentences[0] + m1
    else:
        m0 = masker_sentences[0].resize(masker_sentences[1].n_samples)
        masker_left = masker_sentences[1] + m0
    if masker_sentences[2].n_samples > masker_sentences[3].n_samples:
        m3 = masker_sentences[3].resize(masker_sentences[2].n_samples)
        masker_right = masker_sentences[2] + m3
    else:
        m2 = masker_sentences[2].resize(masker_sentences[3].n_samples)
        masker_right = masker_sentences[3] + m2
    return masker_left, masker_right

#freefield.set_logger('debug') # 'warning' for production
samplerate = 44100
slab.set_default_samplerate(samplerate)
target_dir = Path.cwd() / "olkisa_targets" / "male"
masker_dir = Path.cwd() / "olkisa_masker"
slab.ResultsFile.results_folder = 'Results'
target_files = [file.name for file in target_dir.glob("*")]
masker_files = [file.name for file in masker_dir.glob("*")]

target_level = 70
masker_level = 70
subject_ID = input('Subject ID: ')  # for instance MS01
file = slab.ResultsFile(subject=subject_ID)


proc_list = [['RX81', 'RX8', Path.cwd() / 'rcx' / 'target_masker_buf.rcx'],
           ['RX82', 'RX8', Path.cwd() / 'rcx' / 'target_masker_buf.rcx'],
           ['RP2', 'RP2', freefield.DIR / 'RCX_files' / 'rcx' / 'button.rcx']]
freefield.initialize('dome', device=proc_list)

[target_speaker] = freefield.pick_speakers(23,)
freefield.write(tag='target_ch', value=target_speaker.analog_channel, processors=target_speaker.analog_proc)
masker_speakers = freefield.pick_speakers([15,31,8,38,2,44]) # in pairs, left first



freefield.write(tag='buf_size', value=65311, processors='RX81') # set buf size
freefield.write(tag='buf_size', value=65311, processors='RX82') # set buf size
# 65311 is the number of samples of the longest stimulus
# stims all have different lengths, so the schmidt trigger needs to be set each trial!
# not sure this is done automatically by the write function!

input("Press Enter to start.")

#trials = slab.Trialsequence(conditions=3, n_reps=20)
trials = slab.Trialsequence(conditions=1, n_reps=10)
target_seq = slab.Trialsequence(conditions=target_files, kind='infinite') # returns filename strings
masker_1_seq = slab.Trialsequence(conditions=masker_files, kind='nonrepeating')
maskers = [0,0,0,0]
masker_sentences = [0,0,0,0]

for block in blocks:  # todo 4 blocks
    for trial in trials:
        print(trials.n_remaining)
        # set masker speakers according to trial condition
        #masker_speaker_left, masker_speaker_right = masker_speakers[(trial-1)*2:(trial-1)*2+1]
        # select target
        target = next(target_seq)
        target_sentence = slab.Sound(target_dir / target)
        target_sentence.level = target_level
        # nl = [item for item in target_files if not item[1] is target[1]]  # remove sentences with the middle word of the target
        # select maskers
        # for i in range(4):
        #     # masker = random.choice(nl) # choose a masker randomly
        #
        #     nl = [item for item in nl if not item[0] is masker[0] and not item[1] is masker[1] and not item[2] is masker[2]]
        #     if not nl:
        #         masker = random.choice(stim_files)
        #         raise ValueError('Ran out of options finding maskers!')
        #     maskers[i] = masker
        #     masker_sentence = slab.Sound(stim_dir / (masker+'.wav'))
        #     masker_sentences[i] = masker_sentence
        # #reverse(masker_sentences)
        # masker_left, masker_right = mix(masker_sentences)
        masker_left, masker_right = target = next(masker_seq)  #todo select pairs of maskers from a non repeating list

    masker_left.level = masker_level
    masker_right.level = masker_level

    freefield.write(tag='data_target', value=target_sentence.data, processors=target_speaker.analog_proc)
    freefield.write(tag='data_masker_left', value=masker_left.data, processors=masker_left_speaker.analog_proc)
    freefield.write(tag='data_masker_right', value=masker_right.data, processors=masker_right_speaker.analog_proc)

    # time.sleep(0.1)# DELETE ON FREEFIELD PC!!
    play(target_sentence,0,'0.wav')# DELETE ON FREEFIELD PC!!
    play(masker_left,-90,'1.wav')# DELETE ON FREEFIELD PC!!
    play(masker_right,90,'2.wav')# DELETE ON FREEFIELD PC!!

    #freefield.play()
    with slab.key('number of mistakes:') as key:# DELETE ON FREEFIELD PC!!
        response = key.getch()# DELETE ON FREEFIELD PC!!

    #response = freefield.wait_for_button()
    # write trial RCX_files to results file
    trial_data = [trial, target, *maskers, response]
    file.write(trial_data, tag=trials.this_n)

print('Done.')
"""
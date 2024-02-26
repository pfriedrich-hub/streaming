import freefield
import slab
from pathlib import Path
samplerate = 48828

# -- parameter settings: -- #
target_speaker_id = 23
masker_l_speaker_id = 2
masker_r_speaker_id = 44

# -- main script: -- #

# liste der zu initialisierenden prozessoren und dazugehörige rcx files
proc_list = [['RX81', 'RX8', Path.cwd() / 'rcx' / 'streaming_speech.rcx'],
           ['RX82', 'RX8', Path.cwd() / 'rcx' / 'streaming_speech.rcx'],
           ['RP2', 'RP2', Path.cwd() / 'rcx' / '9_buttons.rcx']]
# initialize processors
freefield.initialize(setup='dome', device=proc_list)

# # read sound file for target speech

target_speech = slab.Sound(Path.cwd() / 'OLKISA_targets' / '000.wav')
masker_speech_l = slab.Sound(Path.cwd() / 'OLKISA_masker' / '013.wav 3 kleine Bilder & 197.wav 9 weiße Schuhe.wav')
masker_speech_r = slab.Sound(Path.cwd() / 'OLKISA_masker' / '013.wav 3 kleine Bilder & 200.wav 7 große Blumen.wav')

#todo for i in n_trials: select random wav from the right folder

# write target sound and speaker to corresponding processor
freefield.set_signal_and_speaker(signal=target_speech, speaker=target_speaker_id, equalize=False, data_tag='data_target',
                       chan_tag='target_ch', n_samples_tag='n_target')
#
freefield.set_signal_and_speaker(signal=target_speech, speaker=masker_r_speaker_id, equalize=False, data_tag='data_masker_l',
                       chan_tag='masker_l_ch', n_samples_tag='n_masker_l')

freefield.set_signal_and_speaker(signal=target_speech, speaker=masker_r_speaker_id, equalize=False, data_tag='data_masker_r',
                       chan_tag='masker_r_ch', n_samples_tag='n_masker_r')

# send trigger to play the sound
freefield.play()




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
target_dir = Path.cwd() / "OLKISA_targets" / "male"
masker_dir = Path.cwd() / "OLKISA_masker"
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
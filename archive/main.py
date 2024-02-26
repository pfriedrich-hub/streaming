import time
import freefield
import slab
from pathlib import Path

freefield.set_logger('debug') # 'warning' for production
samplerate = 48828
slab.set_default_samplerate(samplerate)

subject_id = '1'
condition = 'Ears Free'
subject_dir = Path.cwd() / 'Results' / subject_id / condition

proc_list = [['RX81', 'RX8', Path.cwd() / 'rcx' / 'play_noise_buf.rcx'],
            ['RX82', 'RX8', Path.cwd() / 'rcx' / 'play_noise_buf.rcx'],
            ['RP2', 'RP2', freefield.DIR / 'RCX_files' / 'rcx' / 'button.rcx']]
freefield.initialize('dome', device=proc_list)

[target_speaker] = freefield.pick_speakers(23,)
masker_speakers = freefield.pick_speakers([15,31,8,38,2,44]) # in pairs, left first

print(target_speaker.analog_channel)
for speaker in masker_speakers:
    print(speaker.analog_channel)

freefield.write(tag='buf_size', value=, processors='RX81') # set buf size
freefield.write(tag='buf_size', value=, processors='RX82') # set buf size

freefield.write(tag='target_ch', value=target_speaker.analog_channel, processors=target_speaker.analog_proc)
# set channel

input("Press Enter to start.")

trials = slab.Trialsequence()
for trial in trials:
    target_sentence = slab.tone()
    freefield.write(tag='target_sentence', value=target_sentence.data, processors=target_speaker.analog_proc)
    time.sleep(0.1)
    freefield.play()
    freefield.wait_for_button()



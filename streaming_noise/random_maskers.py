

import slab
import random
import noise_levels


maskers = slab.Sound.pinknoise(duration=0.5)
maskers.level = random.choices(noise_levels.maskers)
maskers.filter(frequency=(500, 3999), kind='bp') # bandpass .25 to 4 kHz
maskers.ramp(duration=0.005)
maskers.play()

#target = slab.Sound.pinknoise(duration=0.5)
#target.filter(frequency=(500, 3999), kind='bp') # bandpass .25 to 4 kHz
#target.ramp(duration=0.005)
#target.level = random.choices(list_noises.targets)
#target.play()

target_seq = slab.Trialsequence(conditions=[maskers], n_reps=20)

# spielt bis jetzt nur 60 dB
for i in target_seq:
  detect = maskers
  detect.play()
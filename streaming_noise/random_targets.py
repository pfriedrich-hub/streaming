
import slab
import random
import streaming_noise.noise_levels as noise_levels

non_target_target = slab.Sound.pinknoise(duration=0.5)
non_target_target.filter(frequency=(500, 3999), kind='bp') # bandpass .25 to 4 kHz
non_target_target.ramp(duration=0.005)
non_target_target.level = random.choices(noise_levels.non_targets_targets)
non_target_target.play()

slab.Precomputed()

# target = slab.Sound.pinknoise(duration=0.5)
# target.filter(frequency=(500, 3999), kind='bp') # bandpass .25 to 4 kHz
# target.ramp(duration=0.005)
# target.level = random.choices(list_noises.targets)
# target.play()

target_seq = slab.Trialsequence(conditions=[non_target_target], n_reps=10)

# spielt bis jetzt nur 60 dB
for i in target_seq:
  detect = non_target_target
  detect.play()

import slab
import random
import streaming_noise.dev.noise_levels as noise_levels

levels = random.choice(noise_levels.masker)  # frequencies of the tones # todo ?
seq = slab.Trialsequence(conditions=levels, n_reps=1)  # 10 repetitions per condition
# now we draw elements from the list, generate a tone and play it until we reach the end:
for freq in seq:
  masker = slab.Sound.pinknoise(level=levels)
  masker.play()



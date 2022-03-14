from math import log, e
import numpy as np
import matplotlib.pyplot as plt
from auxiliary import *

def entropy2(labels, base=None):
  """ Computes entropy of label distribution. """

  n_labels = len(labels)

  if n_labels <= 1:
    return 0

  value, counts = np.unique(list(labels), return_counts=True)
  probs = counts / n_labels
  n_classes = np.count_nonzero(probs)

  if n_classes <= 1:
    return 0

  ent = 0.

  # Compute entropy
  base = e if base is None else base
  for i in probs:
    ent -= i * log(i, base)

  return ent

sizes = np.logspace(2, 7, 6)
nSims = 40

generated_strings = []
for i in range(len(sizes)):
  group = []
  for j in range(nSims):
    group.append(convert_to_string('Experiments/3particlestrings/size' + str(int(sizes[i])) + '_' + str(j)))
  generated_strings.append(group)

lengths = [len(group[0]) for group in generated_strings]

random_strings = []
for length in lengths:
  group = []
  for j in range(nSims):
    random = np.random.randint(0, 2, size=length)
    random = [str(r) for r in random]

    group.append(''.join(random))
  random_strings.append(group)

generated_entropies = [round(np.mean([entropy2(string, base=2) for string in group]), 2) for group in generated_strings]
gen_errs = [jacknife_error([entropy2(string, base=2) for string in group]) for group in generated_strings]

random_entropies = [round(np.mean([entropy2(string, base=2) for string in group]), 2) for group in random_strings]
rand_errs = [jacknife_error([entropy2(string, base=2) for string in group]) for group in random_strings]

fig, ax = plt.subplots(figsize=(12, 8))
labels = [str(length) for length in lengths]

x = np.arange(len(labels))
width= 0.35

rects1 = ax.bar(x - width/2, generated_entropies, width, yerr=gen_errs, label='Entropy of collision generated strings')
rects2 = ax.bar(x + width/2, random_entropies, width, yerr=rand_errs, label='Entropy of random generated strings')

ax.set_ylabel('Entropy [bits]')
ax.set_title('Entropy by string length, separated into collisions generated and random generated strings.')
ax.set_xlabel('String length')
ax.set_xticks(x, labels)
ax.set_ylim(0, 1.2)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.savefig('Plots/comparison_graphs/entropy_comparison')
plt.close()
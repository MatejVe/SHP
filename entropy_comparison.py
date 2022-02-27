from math import log, e
import numpy as np
import matplotlib.pyplot as plt

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

def convert_to_string(filepath):
    """Only use on files that strictly contain collide indices."""
    f = open(filepath)
    collisions = []

    f.readline()
    f.readline()

    for line in f.readlines():
        left, right = line.strip().split(' ')
        left = int(left) + 3 if int(left) < 0 else int(left)
        right = int(right) + 3 if int(right) < 0 else int(right)
        collisions.append((left, right))

    string = ''
    crnt = collisions[0]
    for i in range(1, len(collisions)):
        next = collisions[i]

        # If the next particles to collide are 'to the left' encode 0
        # If the next particles to collide are 'to the right' encode 1
        if crnt[0] == next[1]:
            string += '0'
        elif crnt[1] == next[0]:
            string += '1'

        crnt = next
    return string

generated_strings = []
for i in range(10):
    generated_strings.append(convert_to_string('Experiments/3particlestrings/random' + str(i)))

lengths = [len(string) for string in generated_strings]

random_strings = []
for length in lengths:
    random = np.random.randint(0, 2, size=length)
    random = [str(r) for r in random]

    random_strings.append(''.join(random))

generated_entropies = [round(entropy2(string), 2) for string in generated_strings]
random_entropies = [round(entropy2(string), 2) for string in random_strings]

fig, ax = plt.subplots(figsize=(10, 10))
labels = [str(length + 1) for length in lengths]

x = np.arange(len(labels))
width= 0.35

rects1 = ax.bar(x - width/2, generated_entropies, width, label='Entropy of collision generated strings')
rects2 = ax.bar(x + width/2, random_entropies, width, label='Entropy of random generated strings')

ax.set_ylabel('Entropy')
ax.set_title('Entropy by string length, separated into collisions generated and random generated strings.')
ax.set_xlabel('String length')
ax.set_xticks(x, labels)
ax.set_ylim(0, 0.8)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.savefig('Plots/comparison_graphs/entropy_comparison')
plt.close()
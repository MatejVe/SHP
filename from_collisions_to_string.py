import numpy as np
from math import log, e

f = open('Experiments/3particlestrings/random0')
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

def entropy2(labels, base=None):
  """ Computes entropy of label distribution. """

  n_labels = len(labels)

  if n_labels <= 1:
    return 0

  value, counts = np.unique(labels, return_counts=True)
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

print(entropy2([s for s in string]))
from math import log, e
import numpy as np
import matplotlib.pyplot as plt
from auxiliary import *

sizes = np.logspace(2, 5, 4)
nSims = 10

generated_strings = []
for i in range(len(sizes)):
    group = []
    for j in range(nSims):
        string = convert_to_string(
            "particlescollide3_size{}_num{}".format(str(int(sizes[i])), str(j))
        )
        group.append(string)
    generated_strings.append(group)

lengths = [len(group[0]) for group in generated_strings]

random_strings = []
for length in lengths:
    group = []
    for j in range(nSims):
        random = np.random.randint(0, 2, size=length)
        random = [str(r) for r in random]

        group.append("".join(random))
    random_strings.append(group)

generated_entropies = [
    round(np.mean([entropy2(string, base=2) for string in group]), 2)
    for group in generated_strings
]
gen_errs = [
    jacknife_error([entropy2(string, base=2) for string in group])
    for group in generated_strings
]

random_entropies = [
    round(np.mean([entropy2(string, base=2) for string in group]), 2)
    for group in random_strings
]
rand_errs = [
    jacknife_error([entropy2(string, base=2) for string in group])
    for group in random_strings
]

fig, ax = plt.subplots(figsize=(12, 8))
labels = [str(length) for length in lengths]

x = np.arange(len(labels))
width = 0.35

rects1 = ax.bar(
    x - width / 2,
    generated_entropies,
    width,
    yerr=gen_errs,
    label="Entropy of collision generated strings",
)
rects2 = ax.bar(
    x + width / 2,
    random_entropies,
    width,
    yerr=rand_errs,
    label="Entropy of random generated strings",
)

ax.set_ylabel("Entropy [bits]")
ax.set_title(
    "Entropy by string length, separated into collisions generated and random generated strings."
)
ax.set_xlabel("String length")
ax.set_xticks(x, labels)
ax.set_ylim(0, 1.2)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.savefig("Plots/comparison_graphs/entropy_comparison")
plt.close()

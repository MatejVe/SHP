import numpy as np
import matplotlib.pyplot as plt
import sys
from auxiliary import *

encoder = RunLengthEncoder()

sizes = np.logspace(2, 5, 4)
nSims = 10

generated_sizes = []
compressed_generated = []
for i in range(len(sizes)):
    gen_sized = []
    comp_gen_sized = []
    for j in range(nSims):
        string = convert_to_string(
            "particlescollide3_size{}_num{}".format(str(int(sizes[i])), str(j))
        )
        size = len(string)
        comp_size = len(encoder.encode_b(string))

        gen_sized.append(size)
        comp_gen_sized.append(comp_size)

    generated_sizes.append(gen_sized)
    compressed_generated.append(comp_gen_sized)

lengths = [int(size) for size in sizes]

random_sizes = []
compressed_random = []
for length in lengths:
    rand_sized = []
    comp_rand_sized = []
    for j in range(nSims):
        random = np.random.randint(0, 2, size=length)
        random = "".join([str(r) for r in random])
        size = len(random)
        comp_size = len(encoder.encode_b(random))

        rand_sized.append(size)
        comp_rand_sized.append(comp_size)

    random_sizes.append(rand_sized)
    compressed_random.append(comp_rand_sized)

# Find means and stds
gen_size_means = [np.mean(sized) for sized in generated_sizes]
rand_size_means = [np.mean(sized) for sized in random_sizes]

gen_comp_means = [np.mean(sized) for sized in compressed_generated]
rand_comp_means = [np.mean(sized) for sized in compressed_random]

percentage_generated = [
    [round(gen_comp / gen, 2) for gen_comp in sized]
    for gen, sized in zip(gen_size_means, compressed_generated)
]
percentage_random = [
    [round(rand_comp / rand, 2) for rand_comp in sized]
    for rand, sized in zip(rand_size_means, compressed_random)
]

perc_gen_means = [round(np.mean(size), 2) for size in percentage_generated]
perc_gen_stds = [jacknife_error(size) for size in percentage_generated]

perc_rand_means = [round(np.mean(size), 2) for size in percentage_random]
perc_rand_stds = [jacknife_error(size) for size in percentage_random]


fig, ax = plt.subplots(figsize=(12, 8))
labels = [str(length) for length in lengths]

x = np.arange(len(labels))
width = 0.35

rects1 = ax.bar(
    x - width / 2,
    perc_gen_means,
    width,
    yerr=perc_gen_stds,
    label="Compression ratio \nof generated strings",
)
rects2 = ax.bar(
    x + width / 2,
    perc_rand_means,
    width,
    yerr=perc_rand_stds,
    label="Compression ratio \nof random strings",
)

ax.set_ylabel("Compression ratio")
ax.set_title(
    "Compression ratio by length, compressed/uncompressed, custom algorithm \nseparated into collisions generated strings and random generated strings."
)
ax.set_xlabel("String length")
ax.set_xticks(x, labels)
ax.set_ylim(0, 1.2)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.savefig("Plots/comparison_graphs/compression_customb_comparison")
plt.close()

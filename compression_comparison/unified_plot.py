import numpy as np
import matplotlib.pyplot as plt
import sys
import zlib
import bz2
import time

from auxiliary import *

encoder = RunLengthEncoder()

sizes = np.logspace(2, 7, 6)
nSims = 40

# Find entropy, zlib, bz2 compression percentage, and custom compression
# percentage
generated_zlib_percs = []
generated_bz2_percs = []
generated_encoder_percs = []
generated_entropy = []

for i in range(len(sizes)):
    zlib_row = []
    bz2_row = []
    encoder_row = []
    entropy_row = []

    for j in range(nSims):
        print(f"Processed {(i*40+j)/(40*6)*100}% of generated strings.")
        print(f"Processing size {i}, number {j}.")

        start_time = time.time()
        string = convert_to_string_file(
            "Experiments/3particlestrings/size{}_{}".format(str(int(sizes[i])), str(j))
        )
        bites = read_bytes_from_file(
            "Experiments/3particlestrings/bites{}_{}".format(str(int(sizes[i])), str(j))
        )
        end_time = time.time()
        print(
            f"It took me {end_time-start_time:.2f}s to read in the string and the bites object."
        )

        size = sys.getsizeof(bites)
        string_length = len(string)

        comp_zlib = sys.getsizeof(zlib.compress(bites))
        comp_bz2 = sys.getsizeof(bz2.compress(bites))
        comp_custom = len(encoder.encode_b(string))

        zlib_row.append(100 * comp_zlib / size)
        bz2_row.append(100 * comp_bz2 / size)
        encoder_row.append(100 * comp_custom / string_length)
        entropy_row.append(entropy2(string, base=2))

    generated_zlib_percs.append(zlib_row)
    generated_bz2_percs.append(bz2_row)
    generated_encoder_percs.append(encoder_row)
    generated_entropy.append(entropy_row)

lengths = [int(size) for size in sizes]

# Find  entropy, zlib, bz2 compression percentage, and custom compression
# percentage for random strings
random_zlib_percs = []
random_bz2_percs = []
random_encoder_percs = []
random_entropy = []

for i in range(len(sizes)):
    zlib_row = []
    bz2_row = []
    encoder_row = []
    entropy_row = []

    for j in range(nSims):
        print(f"Processed {(i*40+j)/(40*6)*100}% of random strings.")
        print(f"Processing {i}, number {j}.")

        start_time = time.time()
        randomString = "".join(
            [str(r) for r in np.random.randint(0, 2, size=lengths[i])]
        )
        bites = read_bytes_from_file(
            "Experiments/3particlestrings/randombites{}_{}".format(
                str(int(sizes[i])), str(j)
            )
        )
        end_time = time.time()
        print(
            f"It took me {end_time-start_time:.2f}s to read in the random string and bites."
        )

        size = sys.getsizeof(bites)
        string_length = len(randomString)

        comp_zlib = sys.getsizeof(zlib.compress(bites))
        comp_bz2 = sys.getsizeof(bz2.compress(bites))
        comp_custom = len(encoder.encode_b(randomString))

        zlib_row.append(100 * comp_zlib / size)
        bz2_row.append(100 * comp_bz2 / size)
        encoder_row.append(100 * comp_custom / string_length)
        entropy_row.append(entropy2(randomString, base=2))

    random_zlib_percs.append(zlib_row)
    random_bz2_percs.append(bz2_row)
    random_encoder_percs.append(encoder_row)
    random_entropy.append(entropy_row)

# Plot entropy comparison
gen_ent = [round(np.mean(group), 2) for group in generated_entropy]
gen_ent_errs = [jacknife_error(group) for group in generated_entropy]
rand_ent = [round(np.mean(group), 2) for group in random_entropy]
rand_ent_errs = [jacknife_error(group) for group in random_entropy]

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
labels = [str(length) for length in lengths]
x = np.arange(len(labels))
width = 0.35

ax = axes[0][0]
rects1 = ax.bar(
    x - width / 2,
    gen_ent,
    width,
    yerr=gen_ent_errs,
    label="Collision generated strings",
)
rects2 = ax.bar(
    x + width / 2, rand_ent, width, yerr=rand_ent_errs, label="Random strings"
)
ax.set_ylabel("Entropy [bits]")
ax.set_title("Entropy by string length")
ax.set_xlabel("String length")
ax.set_xticks(x, labels)
ax.set_ylim(0, 1.4)
ax.legend()
ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

# Plot zlib compression percentage
generated_zlib_means = [round(np.mean(size), 2) for size in generated_zlib_percs]
random_zlib_means = [round(np.mean(size), 2) for size in random_zlib_percs]

generated_zlib_stds = [jacknife_error(size) for size in generated_zlib_percs]
random_zlib_stds = [jacknife_error(size) for size in random_zlib_percs]

ax = axes[0][1]
rects1 = ax.bar(
    x - width / 2,
    generated_zlib_means,
    width,
    yerr=generated_zlib_stds,
    label="Collision generated strings",
)
rects2 = ax.bar(
    x + width / 2,
    random_zlib_means,
    width,
    yerr=random_zlib_stds,
    label="Random strings",
)
ax.set_ylabel("Compression percentage")
ax.set_title("Compression percentage by length, \n zlib compression algorithm")
ax.set_xlabel("String length")
ax.set_xticks(x, labels)
ax.set_ylim(0, 130)
ax.legend()
ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

# Plot bz2 compression percentage
generated_bz2_means = [round(np.mean(size), 2) for size in generated_bz2_percs]
random_bz2_means = [round(np.mean(size), 2) for size in random_bz2_percs]

generated_bz2_stds = [jacknife_error(size) for size in generated_bz2_percs]
random_bz2_stds = [jacknife_error(size) for size in random_bz2_percs]

ax = axes[1][0]
rects1 = ax.bar(
    x - width / 2,
    generated_bz2_means,
    width,
    yerr=generated_bz2_stds,
    label="Collision generated strings",
)
rects2 = ax.bar(
    x + width / 2, random_bz2_means, width, yerr=random_bz2_stds, label="Random strings"
)
ax.set_ylabel("Compression percentage")
ax.set_title("Compression percentage by length, \n bz2 compression algorithm")
ax.set_xlabel("String length")
ax.set_xticks(x, labels)
ax.set_ylim(0, 210)
ax.legend()
ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

# Plot custom compression algorithm compression percentage
generated_custom_means = [round(np.mean(size), 2) for size in generated_encoder_percs]
random_custom_means = [round(np.mean(size), 2) for size in random_encoder_percs]

generated_custom_stds = [jacknife_error(size) for size in generated_encoder_percs]
random_custom_stds = [jacknife_error(size) for size in random_encoder_percs]

ax = axes[1][1]
rects1 = ax.bar(
    x - width / 2,
    generated_custom_means,
    width,
    yerr=generated_custom_stds,
    label="Collision generated strings",
)
rects2 = ax.bar(
    x + width / 2,
    random_custom_means,
    width,
    yerr=random_custom_stds,
    label="Random strings",
)
ax.set_ylabel("Compression percentage")
ax.set_title("Compression percentage by length, custom compression algorithm")
ax.set_xlabel("String length")
ax.set_xticks(x, labels)
ax.set_ylim(0, 130)
ax.legend()
ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()
plt.savefig("Plots/comparison_graphs/unified_comparison")
plt.close()

import numpy as np
import matplotlib.pyplot as plt
import sys
import zlib
import bz2

from auxiliary import *

encoder = RunLengthEncoder()

sizes = np.logspace(2, 5, 4)
nSims = 10

generated_sizes = []
zlib_generated = []
bz2_generated = []
encoder_generated = []
entropy_generated = []

for i in range(len(sizes)):
    gen_row = []
    zlib_row = []
    bz2_row = []
    encoder_row = []
    entropy_row = []

    for j in range(nSims):
        string = convert_to_string(
            "particlescollide3_size{}_num{}".format(str(int(sizes[i])), str(j))
        )
        bites = convert_to_bytes_object(string)
        gen_row.append(sys.getsizeof(bites))
        zlib_row.append(sys.getsizeof(zlib.compress(bites)))
        bz2_row.append(sys.getsizeof(bz2.compress(bites)))
        encoder_row.append(len(encoder.encode_b(string)))
        entropy_row.append(entropy2(string, base=2))

    generated_sizes.append(gen_row)
    zlib_generated.append(zlib_row)
    bz2_generated.append(bz2_row)
    encoder_generated.append(encoder_row)
    entropy_generated.append(entropy_row)

lengths = [int(size) for size in sizes]

rand_sizes = []
zlib_random = []
bz2_random = []
encoder_random = []
entropy_random = []

for length in lengths:
    rand_row = []
    zlib_row = []
    bz2_row = []
    encoder_row = []
    entropy_row = []
    for j in range(nSims):
        randomString = "".join([str(r) for r in np.random.randint(0, 2, size=length)])
        bites = convert_to_bytes_object(randomString)
        rand_row.append(sys.getsizeof(bites))
        zlib_row.append(sys.getsizeof(zlib.compress(bites)))
        bz2_row.append(sys.getsizeof(bz2.compress(bites)))
        encoder_row.append(len(encoder.encode_b(randomString)))
        entropy_row.append(entropy2(randomString, base=2))

    rand_sizes.append(rand_row)
    zlib_random.append(zlib_row)
    bz2_random.append(bz2_row)
    encoder_random.append(encoder_row)
    entropy_random.append(entropy_row)

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
labels = [str(length) for length in lengths]
x = np.arange(len(labels))
width = 0.35

gen_ent = [round(np.mean([e for e in group]), 2) for group in entropy_generated]
gen_ent_errs = [jacknife_error(group) for group in entropy_generated]
rand_ent = [round(np.mean([e for e in group]), 2) for group in entropy_random]
rand_ent_errs = [jacknife_error(group) for group in entropy_random]

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

zlib_gen_perc, zlib_gen_errs = percentage_and_error(generated_sizes, zlib_generated)
zlib_gen_perc = [round(i, 2) for i in zlib_gen_perc]
zlib_rand_perc, zlib_rand_errs = percentage_and_error(rand_sizes, zlib_random)
zlib_rand_perc = [round(i, 2) for i in zlib_rand_perc]
ax = axes[0][1]
rects1 = ax.bar(
    x - width / 2,
    zlib_gen_perc,
    width,
    yerr=zlib_gen_errs,
    label="Collision generated strings",
)
rects2 = ax.bar(
    x + width / 2, zlib_rand_perc, width, yerr=zlib_rand_errs, label="Random strings"
)
ax.set_ylabel("Compression percentage")
ax.set_title("Compression percentage by length, \n zlib compression algorithm")
ax.set_xlabel("String length")
ax.set_xticks(x, labels)
ax.set_ylim(0, 1.4)
ax.legend()
ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

bz2_gen_perc, bz2_gen_errs = percentage_and_error(generated_sizes, bz2_generated)
bz2_gen_perc = [round(i, 2) for i in bz2_gen_perc]
bz2_rand_perc, bz2_rand_errs = percentage_and_error(rand_sizes, bz2_random)
bz2_rand_perc = [round(i, 2) for i in bz2_rand_perc]
ax = axes[1][0]
rects1 = ax.bar(
    x - width / 2,
    bz2_gen_perc,
    width,
    yerr=bz2_gen_errs,
    label="Collision generated strings",
)
rects2 = ax.bar(
    x + width / 2, bz2_rand_perc, width, yerr=bz2_rand_errs, label="Random strings"
)
ax.set_ylabel("Compression percentage")
ax.set_title("Compression percentage by length, \n bz2 compression algorithm")
ax.set_xlabel("String length")
ax.set_xticks(x, labels)
ax.set_ylim(0, 2.2)
ax.legend()
ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

ax = axes[1][1]
encoder_gen_perc, encoder_gen_errs = percentage_and_error(
    generated_sizes, encoder_generated
)
encoder_gen_perc = [round(i, 2) for i in encoder_gen_perc]
encoder_rand_perc, encoder_rand_errs = percentage_and_error(rand_sizes, encoder_random)
encoder_rand_perc = [round(i, 2) for i in encoder_rand_perc]
rects1 = ax.bar(
    x - width / 2,
    encoder_gen_perc,
    width,
    yerr=encoder_gen_errs,
    label="Collision generated strings",
)
rects2 = ax.bar(
    x + width / 2,
    encoder_rand_perc,
    width,
    yerr=encoder_rand_errs,
    label="Random strings",
)
ax.set_ylabel("Compression percentage")
ax.set_title("Compression percentage by length, custom compression algorithm")
ax.set_xlabel("String length")
ax.set_xticks(x, labels)
# ax.set_ylim(0, 1.4)
ax.legend()
ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()
plt.savefig("Plots/comparison_graphs/unified_comparison")
plt.close()

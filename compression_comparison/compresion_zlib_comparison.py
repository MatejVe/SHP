import numpy as np
import matplotlib.pyplot as plt
import sys
import zlib
from auxiliary import *

# I chose to do experiments with 10 different sizes, arranged in 100000*(i+1) and within each size 20 experiments

sizes = np.logspace(2, 7, 6)
nSims = 40

generated_sizes = []
compressed_generated = []
for i in range(len(sizes)):
    gen_sized = []
    comp_gen_sized = []
    for j in range(nSims):
        string = convert_to_string('Experiments/3particlestrings/size' + str(int(sizes[i])) + '_' + str(j))
        size = sys.getsizeof(string.encode())
        comp_size = sys.getsizeof(zlib.compress(string.encode()))

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
        random = ''.join([str(r) for r in random])
        size = sys.getsizeof(random.encode())
        comp_size = sys.getsizeof(zlib.compress(random.encode()))

        rand_sized.append(size)
        comp_rand_sized.append(comp_size)
    
    random_sizes.append(rand_sized)
    compressed_random.append(comp_rand_sized)

# Find means and stds
gen_size_means = [np.mean(sized) for sized in generated_sizes]
rand_size_means = [np.mean(sized) for sized in random_sizes]

gen_comp_means = [np.mean(sized) for sized in compressed_generated]
rand_comp_means = [np.mean(sized) for sized in compressed_random]

percentage_generated = [[round(gen_comp/gen, 2) for gen_comp in sized] for gen, sized in zip(gen_size_means, compressed_generated)]
percentage_random = [[round(rand_comp/rand, 2) for rand_comp in sized] for rand, sized in zip(rand_size_means, compressed_random)]

perc_gen_means = [round(np.mean(size), 2) for size in percentage_generated]
perc_gen_stds = [jacknife_error(size) for size in percentage_generated]

perc_rand_means = [round(np.mean(size), 2) for size in percentage_random]
perc_rand_stds = [jacknife_error(size) for size in percentage_random]


fig, ax = plt.subplots(figsize=(12, 8))
labels = [str(length) for length in lengths]

x = np.arange(len(labels))
width= 0.35

rects1 = ax.bar(x - width/2, perc_gen_means, width, yerr=perc_gen_stds, label='Compression ratio \nof generated strings')
rects2 = ax.bar(x + width/2, perc_rand_means, width, yerr=perc_rand_stds, label='Compression ratio \nof random strings')

ax.set_ylabel('Compression ratio')
ax.set_title('Compression ratio by length, uncompressed/compressed, zlib \nseparated into collisions generated strings and random generated strings.')
ax.set_xlabel('String length')
ax.set_xticks(x, labels)
ax.set_ylim(0, 1.2)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.savefig('Plots/comparison_graphs/compression_zlib_comparison')
plt.close()
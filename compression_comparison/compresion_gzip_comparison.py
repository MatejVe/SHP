import numpy as np
import matplotlib.pyplot as plt
import sys
import zlib
from auxiliary import *

# I chose to do experiments with 10 different sizes, arranged in 100000*(i+1) and within each size 20 experiments

lengths = [100000*(i+1) for i in range(10)]

generated_sizes = []
compressed_generated = []
for i in range(10):
    gen_sized = []
    comp_gen_sized = []
    for j in range(40):
        string = convert_to_string('Experiments/3particlestrings/size' + str(100000*(i+1)) + '_' + str(j))
        size = sys.getsizeof(string.encode())
        comp_size = sys.getsizeof(zlib.compress(string.encode()))

        gen_sized.append(size)
        comp_gen_sized.append(comp_size)

    generated_sizes.append(gen_sized)
    compressed_generated.append(comp_gen_sized)


random_sizes = []
compressed_random = []
for length in lengths:
    rand_sized = []
    comp_rand_sized = []
    for j in range(40):
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

percentage_generated = [[round(gen/gen_comp, 2) for gen_comp in sized] for gen, sized in zip(gen_size_means, compressed_generated)]
percentage_random = [[round(rand/rand_comp, 2) for rand_comp in sized] for rand, sized in zip(rand_size_means, compressed_random)]

perc_gen_means = [round(np.mean(size), 2) for size in percentage_generated]
perc_gen_stds = [jacknife_error(size) for size in percentage_generated]

perc_rand_means = [round(np.mean(size), 2) for size in percentage_random]
perc_rand_stds = [jacknife_error(size) for size in percentage_random]


fig, ax = plt.subplots(figsize=(10, 10))
labels = [str(length) for length in lengths]

x = np.arange(len(labels))
width= 0.35

rects1 = ax.bar(x - width/2, perc_gen_means, width, yerr=perc_gen_stds, label='Compression ratio \nof generated strings')
rects2 = ax.bar(x + width/2, perc_rand_means, width, yerr=perc_rand_stds, label='Compression ratio \nof random strings')

ax.set_ylabel('Compression ratio')
ax.set_title('Compression ratio by length, uncompressed/compressed, gzip \nseparated into collisions generated strings and random generated strings.')
ax.set_xlabel('String length')
ax.set_xticks(x, labels)
# ax.set_ylim(0, 0.2)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.savefig('Plots/comparison_graphs/compression_gzip_comparison')
plt.close()
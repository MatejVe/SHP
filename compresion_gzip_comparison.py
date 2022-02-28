import numpy as np
import matplotlib.pyplot as plt
import sys
import zlib

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

# I chose to do experiments with 10 different sizes, arranged in 100000*(i+1) and within each size 20 experiments

generated_strings = []
for i in range(10):
    single_size_strings = []
    for j in range(20):
        single_size_strings.append(convert_to_string('Experiments/3particlestrings/size' + str(100000*(i+1)) + '_' + str(j)))

    generated_strings.append(single_size_strings)

lengths = [100000*(i+1) for i in range(10)]

random_strings = []
for length in lengths:
    single_size_strings = []
    for j in range(20):
        random = np.random.randint(0, 2, size=length)
        random = [str(r) for r in random]

        single_size_strings.append(''.join(random))
    random_strings.append(single_size_strings)

# find original size
generated_sizes = [[sys.getsizeof(string) for string in sized] for sized in generated_strings]
random_sizes = [[sys.getsizeof(string) for string in sized] for sized in random_strings]

# find compresed sizes
compressed_generated = [[sys.getsizeof(zlib.compress(string.encode())) for string in sized] for sized in generated_strings]
compressed_random = [[sys.getsizeof(zlib.compress(string.encode())) for string in sized] for sized in random_strings]

# Find means and stds
gen_size_means = [np.mean(sized) for sized in generated_sizes]
rand_size_means = [np.mean(sized) for sized in random_sizes]

gen_comp_means = [np.mean(sized) for sized in compressed_generated]
rand_comp_means = [np.mean(sized) for sized in compressed_random]

percentage_generated = [[round(gen/gen_comp, 2) for gen_comp in sized] for gen, sized in zip(gen_size_means, compressed_generated)]
percentage_random = [[round(rand/rand_comp, 2) for rand_comp in sized] for rand, sized in zip(rand_size_means, compressed_random)]

perc_gen_means = [round(np.mean(size), 2) for size in percentage_generated]
perc_gen_stds = [np.std(size) for size in percentage_generated]  # TODO: update std with a different method, e.g. jackknife sampling

perc_rand_means = [round(np.mean(size), 2) for size in percentage_random]
perc_rand_stds = [np.std(size) for size in percentage_random]


fig, ax = plt.subplots(figsize=(10, 10))
labels = [str(length) for length in lengths]

x = np.arange(len(labels))
width= 0.35

rects1 = ax.bar(x - width/2, perc_gen_means, width, yerr=perc_gen_stds, label='Compression ratio \nof generated strings')
rects2 = ax.bar(x + width/2, perc_rand_means, width, yerr=perc_rand_stds, label='Compression ratio \nof random strings')

ax.set_ylabel('Compression ratio')
ax.set_title('Compression ratio by length, \nseparated into collisions generated strings and random generated strings.')
ax.set_xlabel('String length')
ax.set_xticks(x, labels)
# ax.set_ylim(0, 0.2)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.savefig('Plots/comparison_graphs/compression_gzip_comparison')
plt.close()
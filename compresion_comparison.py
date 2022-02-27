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

generated_strings = []
for i in range(10):
    generated_strings.append(convert_to_string('Experiments/3particlestrings/random' + str(i)))

lengths = [len(string) for string in generated_strings]

random_strings = []
for length in lengths:
    random = np.random.randint(0, 2, size=length)
    random = [str(r) for r in random]

    random_strings.append(''.join(random))

# find original sizes
generated_sizes = [sys.getsizeof(string) for string in generated_strings]
random_sizes = [sys.getsizeof(string) for string in random_strings]

# find compresed sizes
compressed_generated = [sys.getsizeof(zlib.compress(string.encode())) for string in generated_strings]
compressed_random = [sys.getsizeof(zlib.compress(string.encode())) for string in random_strings]

# find the compression percentage
percentage_generated = [round(gen_comp/gen, 3) for gen_comp, gen in zip(compressed_generated, generated_sizes)]
percentage_random = [round(rand_comp/rand, 3) for rand_comp, rand in zip(compressed_random, random_sizes)]

lengths = [len(string) for string in generated_strings]

fig, ax = plt.subplots(figsize=(10, 10))
labels = [str(length + 1) for length in lengths]

x = np.arange(len(labels))
width= 0.35

rects1 = ax.bar(x - width/2, percentage_generated, width, label='Compression ratio \nof generated strings')
rects2 = ax.bar(x + width/2, percentage_random, width, label='Compression ratio \nof random strings')

ax.set_ylabel('Compression ratio')
ax.set_title('Compression ratio by length, \nseparated into collisions generated strings and random generated strings.')
ax.set_xlabel('String length')
ax.set_xticks(x, labels)
ax.set_ylim(0, 0.2)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.savefig('Plots/comparison_graphs/compression_comparison')
plt.close()
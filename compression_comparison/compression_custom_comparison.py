import numpy as np
import matplotlib.pyplot as plt
import sys
from auxiliary import *

class RunLengthEncoder:

    """
    class containing 3 methods that can be used to return a run-length
    encoded string.
    """

    def encode_a(self, text):

        """
        Returns a run-length encoded string from an input string.
        Note: This function will not return the character count in the return
        string if only a single instance of the character is found.

        Args:
            text (str): A string to encode

        Returns:
            str: A run length encoded string

        Example:
            input: "aaabbcdddd"
            returns: "3a2bc4d"
        """

        count = 1
        previous = ""
        mapping = list()

        for character in text:
            if character != previous:
                if previous:
                    mapping.append((previous, count))
                count = 1
                previous = character
            else:
                count += 1
        else:
            mapping.append((character, count))

        result = ""

        for character, count in mapping:
            if count == 1:
                result += character
            else:
                result += str(count)
                result += character

        return result

    def encode_b(self, text):

        """
        Returns a run-length encoded string from an input string.

        Args:
            text (str): A string to encode

        Returns:
            str: A run length encoded string

        Example:
            input: "aaabbcdddd"
            returns: "3a2b1c4d"
        """

        count = 1
        previous = ""
        mapping = list()

        for character in text:
            if character != previous:
                if previous:
                    mapping.append((previous, count))
                count = 1
                previous = character
            else:
                count += 1
        else:
            mapping.append((character, count))

        result = ""

        for character, count in mapping:
            result += str(count)
            result += character

        return result

    def encode_c(self, text):

        """
        Returns a run-length encoded string from an input string.
        This method uses a list comprehension to build the return
        string.

        Args:
            text (str): A string to encode

        Returns:
            str: A run length encoded string

        Example:
            input: "aaabbcdddd"
            returns: "3a2b1c4d"
        """

        count = 1
        previous = ""
        mapping = list()

        for character in text:
            if character != previous:
                if previous:
                    mapping.append((previous, count))
                count = 1
                previous = character
            else:
                count += 1
        else:
            mapping.append((character, count))

        result = "".join(f"{str(count)}{character}" for character, count in mapping)

        return result

encoder = RunLengthEncoder()

sizes = np.logspace(2, 7, 6)
nSims = 40

generated_sizes = []
compressed_generated = []
for i in range(len(sizes)):
    gen_sized = []
    comp_gen_sized = []
    for j in range(nSims):
        string = convert_to_string('Experiments/3particlestrings/size' + str(int(sizes[i])) + '_' + str(j))
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
        random = ''.join([str(r) for r in random])
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

percentage_generated = [[round(gen/gen_comp, 2) for gen_comp in sized] for gen, sized in zip(gen_size_means, compressed_generated)]
percentage_random = [[round(rand/rand_comp, 2) for rand_comp in sized] for rand, sized in zip(rand_size_means, compressed_random)]

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
ax.set_title('Compression ratio by length, uncompressed/compressed, custom algorithm \nseparated into collisions generated strings and random generated strings.')
ax.set_xlabel('String length')
ax.set_xticks(x, labels)
# ax.set_ylim(0, 0.2)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.savefig('Plots/comparison_graphs/compression_customb_comparison')
plt.close()
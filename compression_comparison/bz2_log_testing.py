import numpy as np
import matplotlib.pyplot as plt
import sys
import bz2
from auxiliary import *
import time

sizes = np.logspace(2, 7, 6)
nSims = 40

generated_all_percs = []
for i in range(len(sizes)):
    generated_singlesize_percs = []

    for j in range(nSims):
        print(f"Processed {(i*40+j)/(40*6)*100}% of generated strings.")
        print(f"Processing {i}, number {j}.")

        start_time = time.time()
        bites = read_bytes_from_file(
            "Experiments/3particlestrings/bites{}_{}".format(str(int(sizes[i])), str(j))
        )
        end_time = time.time()
        print(
            f"It took me {end_time-start_time:.2f}s to read the bites object in memory."
        )
        size = sys.getsizeof(bites)
        comp_size = sys.getsizeof(bz2.compress(bites))

        generated_singlesize_percs.append(100 * comp_size / size)

    generated_all_percs.append(generated_singlesize_percs)

lengths = [int(size) for size in sizes]

random_all_percs = []
for i in range(len(sizes)):
    random_singlesize_percs = []

    for j in range(nSims):
        print(f"Processed {(i*40+j)/(40*6)*100}% of random strings.")
        print(f"Processing {i}, number {j}.")

        bites = read_bytes_from_file(
            "Experiments/3particlestrings/randombites{}_{}".format(
                str(int(sizes[i])), str(j)
            )
        )
        size = sys.getsizeof(bites)
        comp_size = sys.getsizeof(bz2.compress(bites))

        random_singlesize_percs.append(100 * comp_size / size)

    random_all_percs.append(random_singlesize_percs)

start_time = time.time()
# Find means and stds
generated_percentage_means = [np.mean(size) for size in generated_all_percs]
random_percentage_means = [np.mean(size) for size in random_all_percs]

generated_percentage_stds = [jacknife_error(size) for size in generated_all_percs]
random_percentage_stds = [jacknife_error(size) for size in random_all_percs]

means = [generated_percentage_means, random_percentage_means]
errs = [generated_percentage_stds, random_percentage_stds]
end_time = time.time()
print(
    f"Finding the mean and the standard deviation took me {end_time-start_time:.2f}s."
)

labels = [str(length) for length in lengths]

fig, ax = plt.subplots(figsize=(12, 8))

ax.loglog(lengths, [perc - 100 for perc in random_percentage_means])
ax.set_ylabel("Compression percentage")
ax.set_title("Compression percentage, bz2 compression algorithm\n only random strings")
ax.set_xlabel("Number of bits in the string")
plt.savefig("Plots/bz2_loglog_onlyrandom")
plt.close()

""" styles = [":b", "--r"]
labels = ["Compression percentage \nfor collision generated strings",
          "Compression percentage \nfor random strings"]
for i in range(2):
    ax.loglog(lengths, means[i], styles[i], linewidth=2, label=labels[i])
    
ax.set_ylabel("Compression percentage")
ax.set_title("Compression percentage, bz2 compression algorithm")
ax.set_xlabel("Number of bits in the string")
ax.legend()

fig.tight_layout()
plt.savefig("Plots/bz2_loglog")
plt.close() """
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
end_time = time.time()
print(
    f"Finding the mean and the standard deviation took me {end_time-start_time:.2f}s."
)

labels = [str(length) for length in lengths]

comparative_barplot(
    datas=[generated_percentage_means, random_percentage_means],
    yerrs=[generated_percentage_stds, random_percentage_stds],
    labels=[
        "Compression percentage \nof generated strings",
        "Compression percentage \nof random strings",
    ],
    xticks=labels,
    ylabel="Compression percentage",
    xlabel="Number of bits in the string",
    title="Compression percentage, bz2 compression algorithm",
    filepath="Plots/comparison_graphs/compression_bz2_comparison",
)

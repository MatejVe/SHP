import numpy as np
import matplotlib.pyplot as plt
from auxiliary import *
import time

encoder = RunLengthEncoder()

sizes = np.logspace(2, 7, 6)
nSims = 40

generated_all_percs = []
for i in range(len(sizes)):
    generated_singlesize_percs = []

    for j in range(nSims):
        print(f"Processed {(i*40+j)/(40*6)*100}% of generated strings.")
        print(f"Processing size {i}, number {j}.")

        string = convert_to_string_file(
            "Experiments/3particlestrings/size{}_{}".format(str(int(sizes[i])), str(j))
        )
        size = len(string)

        start_time = time.time()
        comp_size = len(encoder.encode_b(string))
        end_time = time.time()
        print(f"Encoding this string took me {end_time-start_time:.2f}s.")

        generated_singlesize_percs.append(100 * comp_size / size)

    generated_all_percs.append(generated_singlesize_percs)

lengths = [int(size) for size in sizes]

random_all_percs = []
for i in range(len(sizes)):
    random_singlesize_percs = []

    for j in range(nSims):
        print(f"Processed {(i*40+j)/(40*6)*100}% of random strings.")
        print(f"Processing {i}, number {j}.")
        random = np.random.randint(0, 2, size=lengths[i])
        random = "".join([str(r) for r in random])
        size = len(random)
        comp_size = len(encoder.encode_b(random))

        random_singlesize_percs.append(100 * comp_size / size)

    random_all_percs.append(random_singlesize_percs)

# Find means and stds
generated_percentage_means = [np.mean(size) for size in generated_all_percs]
random_percentage_means = [np.mean(size) for size in random_all_percs]

generated_percentage_stds = [jacknife_error(size) for size in generated_all_percs]
random_percentage_stds = [jacknife_error(size) for size in random_all_percs]

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
    title="Compression percentage, custom compression algorithm",
    filepath="Plots/comparison_graphs/compression_customb_comparison",
)

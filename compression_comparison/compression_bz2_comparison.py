import numpy as np
import matplotlib.pyplot as plt
import sys
import bz2
from auxiliary import *

sizes = np.logspace(2, 5, 4)
nSims = 10

generated_sizes = []
compressed_generated = []
for i in range(len(sizes)):
    gen_sized = []
    comp_gen_sized = []
    for j in range(nSims):
        string = convert_to_string(
            "particlescollide3_size{}_num{}".format(str(int(sizes[i])), str(j))
        )
        bites = convert_to_bytes_object(string)
        size = sys.getsizeof(bites)
        comp_size = sys.getsizeof(bz2.compress(bites))

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
        randomString = "".join([str(r) for r in np.random.randint(0, 2, size=length)])
        bites = convert_to_bytes_object(randomString)
        size = sys.getsizeof(bites)
        comp_size = sys.getsizeof(bz2.compress(bites))

        rand_sized.append(size)
        comp_rand_sized.append(comp_size)

    random_sizes.append(rand_sized)
    compressed_random.append(comp_rand_sized)

# Find means and stds
gen_size_means = [np.mean(sized) for sized in generated_sizes]
rand_size_means = [np.mean(sized) for sized in random_sizes]

gen_comp_means = [np.mean(sized) for sized in compressed_generated]
rand_comp_means = [np.mean(sized) for sized in compressed_random]

percentage_generated = [
    [gen_comp / gen for gen_comp in sized]
    for gen, sized in zip(gen_size_means, compressed_generated)
]
percentage_random = [
    [rand_comp / rand for rand_comp in sized]
    for rand, sized in zip(rand_size_means, compressed_random)
]

perc_gen_means = [100*round(np.mean(size), 3) for size in percentage_generated]
perc_gen_stds = [100*jacknife_error(size) for size in percentage_generated]

perc_rand_means = [100*round(np.mean(size), 3) for size in percentage_random]
perc_rand_stds = [100*jacknife_error(size) for size in percentage_random]

labels = [str(length) for length in lengths]

comparative_barplot(
    datas=[perc_gen_means, perc_rand_means],
    yerrs=[perc_gen_stds, perc_rand_stds],
    labels=["Compression percentage \nof generated strings", "Compression percentage \nof random strings"],
    xticks=labels,
    ylabel="Compression percentage",
    xlabel="Number of bits in the string",
    title = "Compression percentage, bz2 compression algorithm",
    filepath="Plots/comparison_graphs/compression_bz2_comparison"
)
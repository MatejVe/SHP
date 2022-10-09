import numpy as np
import matplotlib.pyplot as plt
from auxiliary import *
import secrets

sizes = np.logspace(2, 7, 6)
nSims = 40

generated_strings = []
for i in range(len(sizes)):
    group = []
    for j in range(nSims):
        print(f"Processed {(i*40+j)/(40*6)*100}% of generated strings.")
        print(f"Processing size {i}, number {j}.")

        string = convert_to_string_file(
            "Experiments/3particlestrings/size{}_{}".format(str(int(sizes[i])), str(j))
        )
        group.append(string)
    generated_strings.append(group)

lengths = [len(group[0]) for group in generated_strings]

random_strings = []
for length in lengths:
    group = []
    for j in range(nSims):
        #random = np.random.randint(0, 2, size=length)
        random = [secrets.randbelow(2) for i in range(length)]
        random = [str(r) for r in random]

        group.append("".join(random))
    random_strings.append(group)

generated_entropies = [
    round(np.mean([entropy2(string, base=2) for string in group]), 2)
    for group in generated_strings
]
gen_errs = [
    jacknife_error([entropy2(string, base=2) for string in group])
    for group in generated_strings
]

random_entropies = [
    round(np.mean([entropy2(string, base=2) for string in group]), 2)
    for group in random_strings
]
rand_errs = [
    jacknife_error([entropy2(string, base=2) for string in group])
    for group in random_strings
]

labels = [str(length) for length in lengths]

comparative_barplot(
    datas=[generated_entropies, random_entropies],
    yerrs=[gen_errs, rand_errs],
    labels=[
        "Entropy of collision generated strings",
        "Entropy of random generated strings",
    ],
    xticks=labels,
    ylabel="Entropy [bits]",
    xlabel="Number of bits in the string",
    title="Entropy by number of bits",
    filepath="Plots/comparison_graphs/entropy_comparison",
)

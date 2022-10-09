import matplotlib.pyplot as plt
import numpy as np
from auxiliary import *
import zlib
import sys

generated_sizes = []
generated_compressed = []

for i in range(20):
    size_row = []
    compressed_row = []
    for j in range(20):
        size_column = []
        compressed_column = []
        for k in range(10):
            print(f"Procesing file: i={i}, j={j}, k={k}.")
            string = convert_to_string_file(
                "Experiments/runs_mass_tests2d/index"
                + str(i)
                + "_"
                + str(j)
                + "_"
                + str(k)
            )
            bites = bitstring_to_bytes_compact(string)
            size = sys.getsizeof(bites)
            compressed_size = sys.getsizeof(zlib.compress(bites))

            size_column.append(size)
            compressed_column.append(compressed_size)
            
            print(f"Processed {(i*200+j*10+k)/(10*20*20)*100}%.")

        size_row.append(size_column)
        compressed_row.append(compressed_column)

    generated_sizes.append(size_row)
    generated_compressed.append(compressed_row)

plot = [
    [
        np.mean(
            [
                100 * generated_compressed[i][j][k] / generated_sizes[i][j][k]
                for k in range(10)
            ]
        )
        for i in range(20)
    ]
    for j in range(20)
]
errs = [
    [
        jacknife_error(
            [
                100 * generated_compressed[i][j][k] / generated_sizes[i][j][k]
                for k in range(10)
            ]
        )
        for i in range(20)
    ]
    for j in range(20)
]

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

plot0 = axes[0].contourf(plot, extent=[0, 1, 0, 1], origin="lower")
plt.colorbar(plot0, ax=axes[0])
axes[0].set_title("Compression percentage for zlib vs mass ratios.")
axes[0].set_xlabel("$m_1/m_3$ ratio")
axes[0].set_ylabel("$m_2/m_3$ ratio")

plot1 = axes[1].contourf(errs, extent=[0, 1, 0, 1], origin="lower")
plt.colorbar(plot1, ax=axes[1])
axes[1].set_title("Variance in the compression percentage")
axes[1].set_xlabel("$m_1/m_3$ ratio")
axes[1].set_ylabel("$m_2/m_3$ ratio")

plt.tight_layout()
plt.savefig("Plots/2d_plots/zlib_2d")
plt.close()

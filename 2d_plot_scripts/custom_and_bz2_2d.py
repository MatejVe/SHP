import matplotlib.pyplot as plt
import numpy as np
from auxiliary import *
import bz2
import sys

encoder = RunLengthEncoder()

customs = []
bz2s = []

for i in range(20):
    rowC = []
    rowB = []
    for j in range(20):
        columnC = []
        columnB = []
        for k in range(10):
            string = convert_to_string(
                "Experiments/runs_mass_tests2d/index"
                + str(i)
                + "_"
                + str(j)
                + "_"
                + str(k)
            )
            sizeC = len(string)
            sizeB = sys.getsizeof(string.encode())
            comp_sizeC = len(encoder.encode_b(string))
            comp_sizeB = sys.getsizeof(bz2.compress(string.encode()))
            columnC.append(comp_sizeC / sizeC)
            columnB.append(comp_sizeB / sizeB)
        rowC.append(columnC)
        rowB.append(columnB)
    customs.append(rowC)
    bz2s.append(rowB)

plotC = [[np.mean(customs[i][j]) for i in range(20)] for j in range(20)]
plotB = [[np.mean(bz2s[i][j]) for i in range(20)] for j in range(20)]

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

plot0 = axes[0].contourf(plotC, extent=[0, 1, 0, 1], origin="lower")
plt.colorbar(plot0, ax=axes[0])
axes[0].set_title("Compression percentage custom algorithm vs mass ratios.")
axes[0].set_xlabel("$m_1/m_3$ ratio")
axes[0].set_ylabel("$m_2/m_3$ ratio")

plot1 = axes[1].contourf(plotB, extent=[0, 1, 0, 1], origin="lower")
plt.colorbar(plot1, ax=axes[1])
axes[1].set_title("Compression percentage bz2 algorithm vs mass ratios.")
axes[1].set_xlabel("$m_1/m_3$ ratio")
axes[1].set_ylabel("$m_2/m_3$ ratio")

plt.tight_layout()
plt.savefig("Plots/2d_plots/custom_bz2_2d")
plt.close()

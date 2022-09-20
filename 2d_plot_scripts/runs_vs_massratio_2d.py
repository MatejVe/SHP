import matplotlib.pyplot as plt
import numpy as np
from auxiliary import *

plt.rcParams["font.size"] = "20"

Zs = []

for i in range(20):
    row = []
    for j in range(20):
        column = []
        for k in range(10):
            string = convert_to_string_file(
                "Experiments/runs_mass_tests2d/index"
                + str(i)
                + "_"
                + str(j)
                + "_"
                + str(k)
            )
            result = runsTest(string)
            if result is not None:
                column.append(abs(result))
        row.append(column)
    Zs.append(row)

plotZs = [[np.mean(Zs[i][j]) for i in range(20)] for j in range(20)]
errs = [[jacknife_error(Zs[i][j]) for i in range(20)] for j in range(20)]

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

plot0 = axes[0].contourf(plotZs, extent=[0, 1, 0, 1], origin="lower")
plt.colorbar(plot0, ax=axes[0])
axes[0].set_title("Runs test Z score vs mass ratios.")
axes[0].set_xlabel("$m_1/m_3$ ratio")
axes[0].set_ylabel("$m_2/m_3$ ratio")

plot1 = axes[1].contourf(errs, extent=[0, 1, 0, 1], origin="lower")
plt.colorbar(plot1, ax=axes[1])
axes[1].set_title("Variance in the Z score of the Runs test")
axes[1].set_xlabel("$m_1/m_3$ ratio")
axes[1].set_ylabel("$m_2/m_3$ ratio")

plt.tight_layout()
plt.savefig("Plots/2d_plots/runs_2d")
plt.close()

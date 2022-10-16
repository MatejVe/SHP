import matplotlib.pyplot as plt
import numpy as np
from auxiliary import *
import matplotlib

sratios = np.linspace(0.08, 0.12, 50)
Zs = []

for i in range(50):
    Zratio = []
    for j in range(40):
        print(f"Processing i={i} and j={j}.")
        string = convert_to_string_file(
            "Experiments/runs_mass_tests1d/index" + str(i) + "_" + str(j)
        )
        result = runsTest(string)
        if result is not None:
            Zratio.append(abs(result))

    Zs.append(Zratio)

plotZs = [np.mean(Zs[i]) for i in range(50)]
errs = [jacknife_error(Zs[i]) for i in range(50)]

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
axes[0].scatter(sratios, plotZs)
axes[0].errorbar(sratios, plotZs, yerr=errs, fmt="o")
axes[0].set_title(
    "Runs test Z score vs mass ratio $m_1/m_3$, \n $m_2/m_3$ is fixed at 0.87, particle 3 mass is 1"
)
axes[0].set_xlabel("Mass ratio $m_1/m_3$")
axes[0].set_ylabel("Z score")

ratios13 = np.linspace(0.08, 0.12, 40)
ratios23 = np.linspace(0.8, 0.9, 40)
Zs = []

for i in range(40):
    row = []
    for j in range(40):
        column = []
        for k in range(10):
            print(f"Processing i={i}, j={j}, k={k}.")
            string = convert_to_string_file(
                "Experiments/runs_2d_zoomzoom/index"
                + str(i)
                + "_"
                + str(j)
                + "_"
                + str(k)
            )
            result = runsTest(string)
            if result is not None:
                column.append(abs(result))
            print(f"Processed {(i*400+j*10+k)/(10*40*40)*100}%.")
        row.append(column)
    Zs.append(row)
plotZs = [[np.mean(Zs[i][j]) for i in range(40)] for j in range(40)]

plot = axes[1].contourf(plotZs, extent=[0.08, 0.12, 0.8, 0.9], origin="lower", cmap=matplotlib.cm.get_cmap('viridis_r'))
plt.colorbar(plot, ax=axes[1])
axes[1].set_title("Runs test Z score in a zoomed-in area")
axes[1].set_xlabel("$m_1/m_3$ ratio")
axes[1].set_ylabel("$m_2/m_3$ ratio")
plt.tight_layout()
plt.savefig("Plots/2d_plots/runs1d_and_zoomzoom")
plt.close()

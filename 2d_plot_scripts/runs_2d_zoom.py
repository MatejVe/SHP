import matplotlib.pyplot as plt
import numpy as np
from auxiliary import *
from simulation import *
import matplotlib

ratios13 = np.linspace(0.05, 0.2, 20)
ratios23 = np.linspace(0.8, 0.9, 20)

""" for i, ratio13 in enumerate(ratios13):
    for j, ratio23 in enumerate(ratios23):
        masses = np.array([ratio13, ratio23, 1])
        for k in range(5):
            vels = 2 * np.random.random(2) - 1
            vels = np.append(
                vels, (-masses[0] * vels[0] - masses[1] * vels[1]) / masses[2]
            )
            experiment = Simulation(
                collisionNumber=10000, particleNumber=3, masses=masses, initVels=vels
            )
            filename = (
                "Experiments/runs_2d_zoom/index" + str(i) + "_" + str(j) + "_" + str(k)
            )
            experiment.run(shouldLog=["collideIndices"], filename=filename) """

Zs = []

for i in range(20):
    row = []
    for j in range(20):
        column = []
        for k in range(5):
            print(f"Processing i={i}, j={j}, k={k}.")
            string = convert_to_string_file(
                "Experiments/runs_2d_zoom/index" + str(i) + "_" + str(j) + "_" + str(k)
            )
            result = runsTest(string)
            if result is not None:
                column.append(abs(result))
            print(f"Processed {(i*100+j*5+k)/(5*20*20)*100}%.")
        row.append(column)
    Zs.append(row)
plotZs = [[np.mean(Zs[i][j]) for i in range(20)] for j in range(20)]

fig, axes = plt.subplots(1, 1, figsize=(9, 6))
plot = axes.contourf(plotZs, extent=[0.05, 0.2, 0.8, 0.9], origin="lower", cmap=matplotlib.cm.get_cmap('viridis_r'))
plt.colorbar(plot, ax=axes)
axes.set_title("Runs test Z score in a zoomed in area")
axes.set_xlabel("$m_1/m_3$ ratio")
axes.set_ylabel("$m_2/m_3$ ratio")
plt.tight_layout()
plt.savefig("Plots/2d_plots/runs_2d_zoom")
plt.close()

import enum
import matplotlib.pyplot as plt
import numpy as np

# from simulation import *
from auxiliary import *

plt.rcParams["font.size"] = "20"

ratios13 = np.linspace(0.01, 1, 20)
ratios23 = np.linspace(0.01, 1, 20)


# for i, ratio13 in enumerate(ratios13):
#    for j, ratio23 in enumerate(ratios23):
#       masses = np.array([ratio13, ratio23, 1])
#       for k in range(10):
#           vels = 2*np.random.random(2) - 1
#           vels = np.append(vels, (-masses[0]*vels[0] - masses[1]*vels[1])/masses[2])
#           experiment = Simulation(collisionNumber=100000, particleNumber=3, masses=masses, initVels=vels)
#           filename = 'Experiments/runs_mass_tests2d/index' + str(i) + '_' + str(j) + '_' + str(k)
#           experiment.run(shouldLog=['collideIndices'], filename=filename)

Zs = []

for i in range(20):
    row = []
    for j in range(20):
        column = []
        for k in range(10):
            string = convert_to_string(
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

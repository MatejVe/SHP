import matplotlib.pyplot as plt
import numpy as np
from auxiliary import *
from simulation import *

ratios13 = np.linspace(0.08, 0.12, 40)
ratios23 = np.linspace(0.8, 0.9, 40)

for i, ratio13 in enumerate(ratios13):
    for j, ratio23 in enumerate(ratios23):
        masses = np.array([ratio13, ratio23, 1])
        for k in range(5):
            vels = 2*np.random.random(2) - 1
            vels = np.append(vels, (-masses[0]*vels[0] - masses[1]*vels[1])/masses[2])
            experiment = Simulation(collisionNumber=10000, particleNumber=3, masses=masses, initVels=vels)
            filename = 'Experiments/runs_2d_zoomzoom/index' + str(i) + '_' + str(j) + '_' + str(k)
            experiment.run(shouldLog=['collideIndices'], filename=filename)

Zs = []

for i in range(40):
    row = []
    for j in range(40):
        column = []
        for k in range(5):
            string = convert_to_string('Experiments/runs_2d_zoomzoom/index' + str(i) + '_' + str(j) + '_' + str(k))
            result = runsTest(string)
            if result is not None:
                column.append(abs(result))
        row.append(column)
    Zs.append(row)
plotZs = [[np.mean(Zs[i][j]) for i in range(20)] for j in range(20)]

fig, axes = plt.subplots(1, 1, figsize=(9, 6))
plot = axes.contourf(plotZs, extent=[0.08, 0.12, 0.8, 0.9], origin='lower')
plt.colorbar(plot, ax=axes)
axes.set_title('Runs test Z score in a zoomed in area')
axes.set_xlabel('$m_1/m_3$ ratio')
axes.set_ylabel('$m_2/m_3$ ratio')
plt.tight_layout()
plt.savefig('Plots/2d_plots/runs_2d_zoomzoom')
plt.close()
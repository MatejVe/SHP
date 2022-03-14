import enum
import matplotlib.pyplot as plt
import numpy as np
from compression_comparison.auxiliary import *
from simulation import *


ratios13 = np.linspace(0.01, 1, 20)
ratios23 = np.linspace(0.01, 1, 20)


for i, ratio13 in enumerate(ratios13):
    for j, ratio23 in enumerate(ratios23):
       masses = np.array([ratio13, ratio23, 1])
       for k in range(10):
           vels = 2*np.random.random(2) - 1
           vels = np.append(vels, (-masses[0]*vels[0] - masses[1]*vels[1])/masses[2])
           experiment = Simulation(collisionNumber=100000, particleNumber=3, masses=masses, initVels=vels)
           filename = 'Experiments/runs_mass_tests2d/index' + str(i) + '_' + str(j) + '_' + str(k)
           experiment.run(shouldLog=['collideIndices'], filename=filename)

Zs = []

for i in range(20):
    row = []
    for j in range(20):
        column = []
        for k in range(10):
            string = convert_to_string('Experiments/runs_mass_tests2d/index' + str(i) + '_' + str(j) + '_' + str(k))
            result = runsTest(string)
            if result is not None:
                column.append(abs(result))
        row.append(column)
    Zs.append(row)

plotZs = [[np.mean(Zs[i][j]) for i in range(20)] for j in range(20)]
errs = [[jacknife_error(Zs[i][j]) for i in range(20)] for j in range(20)]

plt.contourf(plotZs, extent=[0, 1, 0, 1], origin='lower')
plt.colorbar()
plt.title('Runs test Z score vs mass ratios.')
plt.xlabel('$m_1/m_3$ ratio')
plt.ylabel('$m_2/m_3$ ratio')
plt.savefig('runs_vs_massratio_2d')
plt.close()

plt.contourf(errs, extent=[0,1,0,1], origin='lower')
plt.colorbar()
plt.title('Variance in the Z score of the Runs test')
plt.xlabel('$m_1/m_3$ ratio')
plt.ylabel('$m_2/m_3$ ratio')
plt.savefig('runs_2d_variances')
plt.close()
import matplotlib.pyplot as plt
import numpy as np
from compression_comparison.auxiliary import *
from simulation import *


ratios = np.linspace(0.01, 1, 100)

Zs = []

#for i, ratio in enumerate(ratios):
#    masses = np.array([1, 1, ratio])
#    for j in range(50):
#        vels = 2*np.random.random(2) - 1
#        vels = np.append(vels, (-masses[0]*vels[0] - masses[1]*vels[1])/masses[2])
#        experiment = Simulation(collisionNumber=100000, particleNumber=3, masses=masses, initVels=vels)
#        filename = 'Experiments/runs_mass_tests/index' + str(i) + '_' + str(j)
#        experiment.run(shouldLog=['collideIndices'], filename=filename)


for i in range(100):
    ratioZs = []
    for j in range(50):
        string = convert_to_string('Experiments/runs_mass_tests/index' + str(i) + '_' + str(j))
        result = runsTest(string)
        if result is not None:
            ratioZs.append(abs(result))
    Zs.append(ratioZs)

plotZs = [np.mean(Z) for Z in Zs]
errs = [np.std(Z) for Z in Zs]

fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(ratios, plotZs)
ax.errorbar(ratios, plotZs, yerr=errs, fmt='o')
ax.set_title('Runs test Z score vs mass ratio of one particle')
ax.set_xlabel('Mass ratio')
ax.set_ylabel('Z score')
plt.savefig('runs_vs_massratio')
plt.close()
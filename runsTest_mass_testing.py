import enum
import matplotlib.pyplot as plt
import numpy as np
from compression_comparison.auxiliary import *
from simulation import *


# ratios = np.linspace(0.01, 1, 10)
sratios = np.linspace(0.05, 0.25, 100)

Zs = []

for i, ratio13 in enumerate(sratios):
#     for j, ratio23 in enumerate(ratios):
    masses = np.array([ratio13, 1, 1])
    for k in range(40):
        vels = 2*np.random.random(2) - 1
        vels = np.append(vels, (-masses[0]*vels[0] - masses[1]*vels[1])/masses[2])
        experiment = Simulation(collisionNumber=100000, particleNumber=3, masses=masses, initVels=vels)
        filename = 'Experiments/runs_mass_tests1d/index' + str(i) + '_' + str(k) # + '_' + str(k)
        experiment.run(shouldLog=['collideIndices'], filename=filename)


for i in range(100):
    Zratio = []
    #row = []
    for j in range(40):
        #column = []
        #for k in range(10):
        #    string = convert_to_string('Experiments/runs_mass_tests2d/index' + str(i) + '_' + str(j) + '_' + str(k))
        #    result = runsTest(string)
        #    if result is not None:
        #        column.append(abs(result))
        #row.append(column)
        string = convert_to_string('Experiments/runs_mass_tests1d/index' + str(i) + '_' + str(j))
        result = runsTest(string)
        if result is not None:
            Zratio.append(abs(result))

    Zs.append(Zratio)

plotZs = [np.mean(Zs[i]) for i in range(100)]
errs = [np.std(Zs[i]) for i in range(100)]

fig, ax = plt.subplots(figsize=(10, 8))
#plt.imshow(plotZs, extent=[0, 1, 0, 1], origin='lower')
#plt.colorbar()
#plt.title('Runs test Z score vs mass ratios.')
#plt.xlabel('$m_1/m_3$ ratio')
#plt.ylabel('$m_2/m_3$ ratio')
#plt.savefig('runs_vs_massratio_2d')
ax.scatter(sratios, plotZs)
ax.errorbar(sratios, plotZs, yerr=errs, fmt='o')
ax.set_title('Runs test Z score vs mass ratio of one particle, \n other two masses are 1')
ax.set_xlabel('Mass ratio')
ax.set_ylabel('Z score')
plt.savefig('runs_vs_massratio_1d')
plt.close()
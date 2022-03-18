import enum
import matplotlib.pyplot as plt
import numpy as np
from compression_comparison.auxiliary import *
from simulation import *

sratios = np.linspace(0.05, 0.25, 50)

Zs = []

#for i, ratio13 in enumerate(sratios):
#    masses = np.array([ratio13, 0.8, 1])
#    for k in range(40):
#        vels = 2*np.random.random(2) - 1
#        vels = np.append(vels, (-masses[0]*vels[0] - masses[1]*vels[1])/masses[2])
#        experiment = Simulation(collisionNumber=100000, particleNumber=3, masses=masses, initVels=vels)
#        filename = 'Experiments/runs_mass_tests1d/index' + str(i) + '_' + str(k)
#        experiment.run(shouldLog=['collideIndices'], filename=filename)


for i in range(50):
    Zratio = []
    for j in range(40):
        string = convert_to_string('Experiments/runs_mass_tests1d/index' + str(i) + '_' + str(j))
        result = runsTest(string)
        if result is not None:
            Zratio.append(abs(result))

    Zs.append(Zratio)

plotZs = [np.mean(Zs[i]) for i in range(50)]
errs = [jacknife_error(Zs[i]) for i in range(50)]

fig, ax = plt.subplots(figsize=(12, 8))
ax.scatter(sratios, plotZs)
ax.errorbar(sratios, plotZs, yerr=errs, fmt='o')
ax.set_title('Runs test Z score vs mass ratio of particle 1, \n particle 2 is 0.8, particle 3 is 1')
ax.set_xlabel('Mass ratio')
ax.set_ylabel('Z score')
plt.savefig('Plots/2d_plots/runs_vs_massratio_1d')
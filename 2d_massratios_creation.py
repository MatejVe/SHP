import numpy as np
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
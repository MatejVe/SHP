from simulation import *
import os
import numpy as np

# print(os.getcwd())

# Let's conduct a bunch of colliding experiments, with randomized positions and velocitites
# Velocities are such that the total momentum ends up being zero

# mass = np.random.random(3) # tried with same mass, maybe changing it will change the results

nSizes = 10

nSims = 20

for i in range(nSizes):
    for j in range(nSims):
        mass = np.random.random(3)
        vels = 2*np.random.random(2) - 1
        vels = np.append(vels, (-mass[0]*vels[0] - mass[1]*vels[1])/mass[2])

        experiment = Simulation(collisionNumber=100000*(i+1), particleNumber=3, masses=mass, initVels=vels)
        filename = 'Experiments/3particlestrings/size' + str(100000*(i+1)) + '_' + str(j)
        experiment.run(shouldLog=['collideIndices'], filename=filename)
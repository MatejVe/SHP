from simulation import *
import os
import numpy as np

# print(os.getcwd())

# Let's conduct a bunch of colliding experiments, with randomized positions and velocitites
# Velocities are such that the total momentum ends up being zero

# mass = np.random.random(3) # tried with same mass, maybe changing it will change the results

sizes = np.logspace(2, 7, 6)

nSims = 40

for i in range(len(sizes)):
    for j in range(nSims):
        mass = np.random.random(3)
        vels = 2*np.random.random(2) - 1
        vels = np.append(vels, (-mass[0]*vels[0] - mass[1]*vels[1])/mass[2])
        poss = np.random.random(3)

        # Save the collision indices
        experiment = Simulation(collisionNumber=int(sizes[i]+1), particleNumber=3, masses=mass, initVels=vels, initPoss=poss)
        filename = 'Experiments/3particlestrings/size' + str(int(sizes[i])) + '_' + str(j)
        experiment.run(shouldLog=['collideIndices'], filename=filename)

        # Save the first few position and velocity data so we can see what is going on
        experiment = Simulation(collisionNumber=10000, particleNumber=3, masses=mass, initVels=vels, initPoss=poss)
        filename = 'Experiments/3_particles/size' + str(sizes[i]) + '_' + str(j)
        experiment.run(shouldLog=['time', 'positions', 'velocities'], filename=filename)
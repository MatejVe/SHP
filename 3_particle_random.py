from simulation import *
import os
import numpy as np

# print(os.getcwd())

# Let's conduct a bunch of colliding experiments, with randomized positions and velocitites
# Velocities are such that the total momentum ends up being zero
mass = np.random.random(3)
vels = 2*np.random.random(2) - 1
vels = np.append(vels, (-mass[0]*vels[0] - mass[1]*vels[1])/mass[2])

nSims = 10

for i in range(nSims):
    experiment = Simulation(collisionNumber=10000, particleNumber=3, masses=mass, initVels=vels)
    filename = 'SHP/Experiments/3_particles/random' + str(i)
    experiment.run(shouldLog=['time', 'positions', 'velocities'], filename=filename)
from simulation import *
import os

print(os.getcwd())

# Let's conduct a bunch of colliding experiments, with randomized positions and velocitites

nSims = 100

for i in range(nSims):
    experiment = Simulation(collisionNumber=10000, particleNumber=3)
    filename = 'SHP/Experiments/3_particles/random' + str(i)
    experiment.run(shouldLog=['time', 'positions', 'velocities'], filename=filename)
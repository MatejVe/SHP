from simulation import *
import numpy as np
import time

# print(os.getcwd())

# Let's conduct a bunch of colliding experiments, with randomized positions and velocitites
# Velocities are such that the total momentum ends up being zero

# mass = np.random.random(3) # tried with same mass, maybe changing it will change the results

sizes = np.logspace(2, 5, 4)

nSims = 10

time1 = time.time()
for i in range(len(sizes)):
    for j in range(nSims):
        time11 = time.time()
        print(f"Simulating size {sizes[i]}, number {j}.")

        mass = np.random.random(3)
        vels = 2 * np.random.random(2) - 1
        vels = np.append(vels, (-mass[0] * vels[0] - mass[1] * vels[1]) / mass[2])
        poss = np.random.random(3)

        # Save the collision indices
        experiment = Simulation(
            collisionNumber=int(sizes[i] + 1),
            particleNumber=3,
            masses=mass,
            initVels=vels,
            initPoss=poss,
        )
        tableName = "particlescollide3_size{}_num{}".format(str(int(sizes[i])), str(j))
        experiment.run(shouldLog=["collideIndices"], tableName=tableName)
        time22 = time.time()
        print(f"It took me {time22-time11:.2f}s to simulate size {sizes[i]}.")
        # Save the first few position and velocity data so we can see what is going on
        # experiment = Simulation(
        #    collisionNumber=10000,
        #    particleNumber=3,
        #    masses=mass,
        #    initVels=vels,
        #    initPoss=poss,
        # )
        # tableName = "3 particles size" + str(sizes[i]) + " " + str(j)
        # experiment.run(shouldLog=["time", "positions", "velocities"], tableName=tableName)
time2 = time.time()
print(f"It took me {time2-time1:.2f}s to simulate all of this.")

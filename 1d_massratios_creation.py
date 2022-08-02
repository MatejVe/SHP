import numpy as np
from simulation import *
import time

sratios = np.linspace(0.08, 0.12, 50)

time1 = time.time()
for i, ratio13 in enumerate(sratios):
    masses = np.array([ratio13, 0.87, 1])
    for k in range(10):
        time11 = time.time()
        print(f"Simulating ratio {sratios[i]}, number {k}.")

        vels = 2 * np.random.random(2) - 1
        vels = np.append(vels, (-masses[0] * vels[0] - masses[1] * vels[1]) / masses[2])
        
        tableName = "massratios1D_index{}_{}".format(str(i), str(k))
        experiment = Simulation(
            collisionNumber=10000, particleNumber=3, masses=masses, initVels=vels
        )
        experiment.run(shouldLog=["collideIndices"], storageType='table', storageName=tableName)
        time22 = time.time()
        print(f"It took me {time22-time11:.2f}s to simulate ratio {ratio13} num {k}.")
time2 = time.time()
print(f"It took me {time2-time1:.2f}s to simulate all of this.")
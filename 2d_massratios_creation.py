import numpy as np
from simulation import *
import time

ratios13 = np.linspace(0.01, 1, 20)
ratios23 = np.linspace(0.01, 1, 20)

for i, ratio13 in enumerate(ratios13):
    for j, ratio23 in enumerate(ratios23):
        masses = np.array([ratio13, ratio23, 1])
        for k in range(10):
            print(f"Simulating i={i}, j={j}, k={k}.")
            vels = 2 * np.random.random(2) - 1
            vels = np.append(
                vels, (-masses[0] * vels[0] - masses[1] * vels[1]) / masses[2]
            )
            
            start_time = time.time()
            experiment = Simulation(
                collisionNumber=100000, particleNumber=3, masses=masses, initVels=vels
            )
            filename = (
                "Experiments/runs_mass_tests2d/index"
                + str(i)
                + "_"
                + str(j)
                + "_"
                + str(k)
            )
            experiment.run(shouldLog=["collideIndices"], storageType="file", storageName=filename)
            end_time = time.time()
            print(f"Took me {end_time-start_time:.2f}s to simulate 100000 collisions.")
            print(f"{(i*200+j*10+k)/(20*20*10)*100:.2f}% done.")

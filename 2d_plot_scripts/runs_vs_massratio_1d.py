import matplotlib.pyplot as plt
import numpy as np
from auxiliary import *
from simulation import *

sratios = np.linspace(0.08, 0.12, 50)

Zs = []

for i, ratio13 in enumerate(sratios):
    masses = np.array([ratio13, 0.87, 1])
    for k in range(40):
        vels = 2*np.random.random(2) - 1
        vels = np.append(vels, (-masses[0]*vels[0] - masses[1]*vels[1])/masses[2])
        experiment = Simulation(collisionNumber=100000, particleNumber=3, masses=masses, initVels=vels)
        filename = 'Experiments/runs_mass_tests1d/index' + str(i) + '_' + str(k)
        experiment.run(shouldLog=['collideIndices'], filename=filename)


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

fig, ax = plt.subplots(figsize=(12, 6))
ax.scatter(sratios, plotZs)
ax.errorbar(sratios, plotZs, yerr=errs, fmt='o')
ax.set_title('Runs test Z score vs mass ratio $m_1/m_3$, \n $m_2/m_3$ is fixed at 0.87, particle 3 mass is 1')
ax.set_xlabel('Mass ratio $m_1/m_3$')
ax.set_ylabel('Z score')
plt.savefig('Plots/2d_plots/runs_vs_massratio_1d')

print(f'Minimum Z score is {min(plotZs)}')
idx = np.argmin(plotZs)
print(f'It occurs for mass ratio $m_1/m_3$ of {sratios[idx]}')
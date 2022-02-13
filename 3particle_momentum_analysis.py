import matplotlib.pyplot as plt
from decimal import Decimal as D

f = open('Experiments/3_particles/random1')
times = []
momenta = [[], [], []]

line1 = f.readline()
masses = [D(mass) for mass in line1.split('|')[1].split(':')[1].strip().split(' ')]

f.readline()

for line in f.readlines():
    times.append(float(line.split('|')[0]))
    vs = line.split('|')[2].split(' ')

    for i in range(3):
        momenta[i].append(D(vs[i]) * masses[i])

f.close()

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.set_title('Momentum probability distributions')
ax.hist(x=momenta[0], color='blue', bins=500, histtype='step', weights=times, density=True)
ax.hist(x=momenta[1], color='red', bins=500, histtype='step', weights=times, density=True)
ax.hist(x=momenta[2], color='green', bins=500, histtype='step', weights=times, density=True)
ax.legend(labels=["Particle 0", "Particle 1", "Particle 2"])

plt.savefig('momentum_distributions')
plt.show()
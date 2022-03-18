import matplotlib.pyplot as plt
from decimal import Decimal as D

for i in range(1):
    f = open('Experiments/3_particles/random' + str(i))
    times = []
    momenta = [[], [], []]
    velocities = [[], [], []]

    line1 = f.readline()
    masses = [D(mass) for mass in line1.split('|')[1].split(':')[1].strip().split(' ')]

    f.readline()

    for line in f.readlines():
        times.append(float(line.split('|')[0]))
        vs = line.split('|')[2].split(' ')

        for j in range(3):
            velocities[j].append(vs[j])
            momenta[j].append(D(vs[j]) * masses[j])

    f.close()

    fig, ax = plt.subplots(2, 1, figsize=(10, 10))
    ax[0].set_title('Momentum probability distributions')
    ax[0].hist(x=momenta[0], color='blue', bins=500, histtype='step', weights=times, density=True)
    ax[0].hist(x=momenta[1], color='red', bins=500, histtype='step', weights=times, density=True)
    ax[0].hist(x=momenta[2], color='green', bins=500, histtype='step', weights=times, density=True)
    ax[0].legend(labels=["Particle 0", "Particle 1", "Particle 2"])

    ax[1].set_title('Velocity probability distributions')
    ax[1].hist(x=velocities[0], color='blue', bins=500, histtype='step', weights=times, density=True)
    ax[1].hist(x=velocities[1], color='red', bins=500, histtype='step', weights=times, density=True)
    ax[1].hist(x=velocities[2], color='green', bins=500, histtype='step', weights=times, density=True)
    ax[1].legend(labels=["Particle 0", "Particle 1", "Particle 2"])

    plt.savefig('Plots/momenta_distributions/momentum__velocity_distribution' + str(i))
    plt.close()
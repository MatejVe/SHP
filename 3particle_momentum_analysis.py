import matplotlib.pyplot as plt
from decimal import Decimal as D

for i in range(10):
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
            velocities[j].append(float(vs[j]))
            momenta[j].append(float(D(vs[j]) * masses[j]))

    f.close()

    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    ax.set_title('Momentum and probability distributions overlayed together')
    ax.hist(x=momenta[0], color='blue', bins=500, histtype='step', weights=times, density=True)
    ax.hist(x=momenta[1], color='red', bins=500, histtype='step', weights=times, density=True)
    ax.hist(x=momenta[2], color='green', bins=500, histtype='step', weights=times, density=True)
    ax.hist(x=velocities[0], color='c', bins=500, histtype='step', weights=times, density=True)
    ax.hist(x=velocities[1], color='m', bins=500, histtype='step', weights=times, density=True)
    ax.hist(x=velocities[2], color='y', bins=500, histtype='step', weights=times, density=True)
    ax.legend(labels=["$P(p_0)$, $m_0=$" + str(round(masses[0], 2)),
                      "$P(p_1)$, $m_1=$" + str(round(masses[1], 2)),
                      "$P(p_2)$, $m_2=$" + str(round(masses[2], 2)),
                      "$P(v_0)$",
                      "$P(v_1)$",
                      "$P(v_2)$"])
    ax.set_xlabel("Arbitrary units, either for velocity or for momentum")
    ax.set_ylabel("Probability")

    plt.savefig('Plots/momenta_distributions/momentum__velocity_distribution' + str(i))
    plt.close()
import matplotlib.pyplot as plt
from decimal import Decimal as D

def convert_to_timestep(filepath):
    f = open(filepath)

    positions = [[], [], []]
    velocities = [[], [], []]

    line1 = f.readline()
    masses = [D(mass) for mass in line1.split('|')[1].split(':')[1].strip().split(' ')]

    f.readline() # skip the second line of the file

    init = f.readline()  # Read initial velocities and positions

    # Transform into timestep positions and velocities
    time = D(init.split('|')[0])
    prevPoss = [D(initPos) for initPos in init.split('|')[1].split(' ')]
    prevVels = [D(initVel) for initVel in init.split('|')[2].split(' ')]
    ts = D('0.01')  # Timestep will be 0.01

    for i in range(int(time // ts)):
        for j in range(3):
            newPos = (prevPoss[j] + (i+1)*ts*prevVels[j]) % 1
            newPos = newPos + D('1') if newPos < 0 else newPos
            positions[j].append(newPos)
            velocities[j].append(prevVels[j])

    leftTime = time % ts

    for line in f.readlines():
        time, poss, vels = line.split('|')[:3]
        time = D(time)
        poss = [D(pos) for pos in poss.split(' ')]
        vels = [D(vel) for vel in vels.split(' ')]

        for i in range(3): # Sort the weird time step
            newPos = (poss[i] + (ts - leftTime)*vels[i]) % 1
            newPos = newPos + D('1') if newPos < 0 else newPos
            positions[i].append(newPos)
            velocities[i].append(vels[i])
        time = time - (ts - leftTime)

        for i in range(int(time // ts)):
            for j in range(3):
                newPos = (poss[j] + (i+1)*ts*vels[j] + (ts - leftTime)*vels[j]) % 1
                newPos = newPos + D('1') if newPos < 0 else newPos
                positions[j].append(newPos)
                velocities[j].append(vels[j])

        leftTime = time % ts
    f.close()

    return masses, positions, velocities

for i in range(2, 10):
    masses, positions, velocities = convert_to_timestep('Experiments/3_particles/random' + str(i))

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))

    axes[0].set_title('Position probability distributions')
    axes[0].set_xlim(0, 1)
    axes[0].hist(x=positions[0], color='blue', bins=1000, histtype='step', density=True)
    axes[0].hist(x=positions[1], color='red', bins=1000, histtype='step', density=True)
    axes[0].hist(x=positions[2], color='green', bins=1000, histtype='step', density=True)
    axes[0].legend(labels=["Particle 0", "Particle 1", "Particle 2"])

    axes[1].set_title('Velocity probability distributions')
    axes[1].hist(x=velocities[0], color='blue', bins=1000, histtype='step', density=True)
    axes[1].hist(x=velocities[1], color='red', bins=1000, histtype='step', density=True)
    axes[1].hist(x=velocities[2], color='green', bins=1000, histtype='step', density=True)
    axes[1].legend(labels=["Particle 0", "Particle 1", "Particle 2"])

    plt.savefig('Plots/Phase_space_distributions/3particles_distribution' + str(i))
    plt.close()
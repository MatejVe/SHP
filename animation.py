from decimal import Decimal as D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.style.use('seaborn-pastel')

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

masses, positions, velocities = convert_to_timestep('Experiments/3_particles/size100000_0')

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 10))
# ax = plt.axes(xlim=(0,1), ylim=(-0.5,0.5))
axes[0].set_xlim(0, 1)
axes[0].set_ylim(-0.25, 0.25)
axes[0].get_yaxis().set_visible(False)
axes[0].set_title('Position Space')
axes[1].set_xlim(-3, 3)
axes[1].set_ylim(-1, 1)
axes[1].get_yaxis().set_visible(False)
axes[1].set_title('Velocity Space')

maxMass = max(masses)
circles = []
colors = ['r', 'b', 'g']

for i in range(3):
    circle1 = plt.Circle((positions[i][0], 0), 
                        radius=D(0.01)*masses[i]/maxMass+D(0.005), 
                        color=colors[i])
    circle2 = plt.Circle((velocities[i][0], 0),
                        radius=D(0.01)*masses[i]/maxMass+D(0.01),
                        color=colors[i])
    circles.append(circle1)
    circles.append(circle2)
    axes[0].add_patch(circle1)
    axes[1].add_patch(circle2)

def animate(i):
    for j in range(3):
        circles[2*j].set(center=(positions[j][i], 0))
        circles[2*j+1].set(center=(velocities[j][i], 0))
    return circles

anim = animation.FuncAnimation(fig, animate, frames=1000, interval=50, blit=True)
anim.save('exampleCollisions.gif', writer='imagemagick', fps=30)
plt.close()


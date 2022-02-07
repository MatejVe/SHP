import os
from decimal import Decimal as D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pandas import Interval
plt.style.use('seaborn-pastel')


# print(os.getcwd())  # C:\Users\matej\Desktop\Year 4 Stuff\Senior Honours Project\SHP
f = open('Experiments/3_particles/random9')
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

fig = plt.figure(figsize=(10, 10))
ax = plt.axes(xlim=(0,1), ylim=(-0.5,0.5))
ax.get_yaxis().set_visible(False)

maxMass = max(masses)
circles = []
colors = ['r', 'b', 'g']

for i in range(3):
    circle = plt.Circle((positions[i][0], 0), 
                        radius=D(0.01)*masses[i]/maxMass+D(0.005), 
                        color=colors[i])
    circles.append(circle)
    ax.add_patch(circle)

def animate(i):
    for j in range(3):
        circles[j].set(center=(positions[j][i], 0))
    return circles

anim = FuncAnimation(fig, animate, frames=10000, interval=10, blit=True)
plt.show()

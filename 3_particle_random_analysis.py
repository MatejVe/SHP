import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

print(os.getcwd())  # C:\Users\matej\Desktop\Year 4 Stuff\Senior Honours Project\SHP

f = open('Experiments/3_particles/random0')

vel0 = []
vel1 = []
vel2 = []

f.readline()
f.readline() # Skip first two rows

for line in f.readlines():
    vels = line.split('|')[2].split(' ')
    vel0.append(float(vels[0]))
    vel1.append(float(vels[1]))
    vel2.append(float(vels[2]))

f.close()

sns.histplot(x=vel0, kde=True, bins=30, stat='density', color='blue')
sns.histplot(x=vel1, kde=True, bins=30, stat='density', color='red')
sns.histplot(x=vel2, kde=True, bins=30, stat='density', color='green')
plt.show()
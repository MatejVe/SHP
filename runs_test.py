import random
import math
import matplotlib.pyplot as plt
import numpy as np
from compression_comparison.auxiliary import *

Zs = []
for i in range(10):
    for j in range(40):
        string = convert_to_string('Experiments/3particlestrings/size' + str(100000*(i+1)) + '_' + str(j))
        Zs.append(abs(runsTest(string)))

fig, ax = plt.subplots(figsize=(10, 10))
ax.hist(Zs, bins=100)
ax.set_title('Runs test Z score distribution')
ax.set_xlabel('Z score')
ax.set_ylabel('Count')
plt.savefig('runsTest_distribution')
plt.close()
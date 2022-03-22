from statsmodels.graphics import tsaplots
import matplotlib.pyplot as plt
import numpy as np
from compression_comparison.auxiliary import *

s1 = convert_to_string('Experiments/3particlestrings/size10000_4')
s1 = [int(e) for e in s1]
s2 = np.random.randint(0, 2, size=10000)

fig = tsaplots.plot_acf(s1, lags=15)
plt.show()
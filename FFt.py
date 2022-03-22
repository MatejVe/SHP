import matplotlib.pyplot as plt
import numpy as np
from compression_comparison.auxiliary import *

s = convert_to_string('Experiments/3particlestrings/size100_3')

s = [int(e) for e in s]
#s = np.random.randint(0, 2, size=100)

tmax = 100
tres = 1
t = np.linspace(0, tmax, tmax*tres, endpoint=False)

plt.plot(t, s)
plt.show()
plt.close()

hh = np.fft.rfft(s)
nn = min(100, hh.size)
freq = np.linspace(0,  (nn-1)/t.max(), nn)

plt.plot(freq, abs(hh[:nn]))
plt.show()
plt.close()
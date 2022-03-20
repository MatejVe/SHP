import matplotlib.pyplot as plt
import numpy as np
from auxiliary import *

encoder = RunLengthEncoder()

customs = []

for i in range(20):
    row = []
    for j in range(20):
        column = []
        for k in range(10):
            string = convert_to_string('Experiments/runs_mass_tests2d/index' + str(i) + '_' + str(j) + '_' + str(k))
            size = len(string)
            comp_size = len(encoder.encode_b(string))
            column.append(comp_size/size)
        row.append(column)
    customs.append(row)

plot = [[np.mean(customs[i][j]) for i in range(20)] for j in range(20)]
errs = [[jacknife_error(customs[i][j]) for i in range(20)] for j in range(20)]

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

plot0 = axes[0].contourf(plot, extent=[0, 1, 0, 1], origin='lower')
plt.colorbar(plot0, ax=axes[0])
axes[0].set_title('Compression percentage custom algorithm vs mass ratios.')
axes[0].set_xlabel('$m_1/m_3$ ratio')
axes[0].set_ylabel('$m_2/m_3$ ratio')

plot1 = axes[1].contourf(errs, extent=[0,1,0,1], origin='lower')
plt.colorbar(plot1, ax=axes[1])
axes[1].set_title('Variance in the compression percentage')
axes[1].set_xlabel('$m_1/m_3$ ratio')
axes[1].set_ylabel('$m_2/m_3$ ratio')

plt.tight_layout()
plt.savefig('Plots/2d_plots/custom_2d')
plt.close()
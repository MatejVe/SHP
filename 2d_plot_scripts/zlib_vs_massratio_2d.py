import matplotlib.pyplot as plt
import numpy as np
from compression_comparison.auxiliary import *
import zlib
import sys

zlibs = []

for i in range(20):
    row = []
    for j in range(20):
        column = []
        for k in range(10):
            string = convert_to_string('Experiments/runs_mass_tests2d/index' + str(i) + '_' + str(j) + '_' + str(k))
            size = sys.getsizeof(string.encode())
            comp_size = sys.getsizeof(zlib.compress(string.encode()))
            column.append(comp_size/size)
        row.append(column)
    zlibs.append(row)

plot = [[np.mean(zlibs[i][j]) for i in range(20)] for j in range(20)]
errs = [[jacknife_error(zlibs[i][j]) for i in range(20)] for j in range(20)]


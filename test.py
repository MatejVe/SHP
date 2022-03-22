from compression_comparison.auxiliary import *
import numpy as np

encoder = RunLengthEncoder()
s = np.random.randint(0, 2, size=100000)
s = ''.join([str(e) for e in s])

print(len(s))
print(len(encoder.encode_b(s)))
print(encoder.encode_b(s)[:100])
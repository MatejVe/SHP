import string
from auxiliary import *
import time
import numpy as np

sizes = np.logspace(2, 7, 6)
nSims = 40

for i in range(len(sizes)):
    for j in range(nSims):
        print(f"Processing {i}, number {j}.")
        print(f"{(i*40+j)/(6*40)*100:.2f}% done.")

        t1 = time.time()
        string = convert_to_string_file_Graeme(
            "Experiments/3particlestrings/size{}_{}".format(str(int(sizes[i])), str(j))
        )
        t2 = time.time()
        print(f"It took me {t2-t1:.2f}s to convert collision history to a string.")

        t1 = time.time()
        bites = bitstring_to_bytes_compact(string)
        t2 = time.time()
        print(f"It took me {t2-t1:.2f}s to convert to a bytes object.")

        t1 = time.time()
        write_to_file_bytes_object(
            bites,
            "Experiments/3particlestrings/Graeme_bites{}_{}".format(
                str(int(sizes[i])), str(j)
            ),
        )
        t2 = time.time()
        print(f"It took me {t2-t1:.2f}s to write down a bites object.")

lengths = [int(size) for size in sizes]

for i, length in enumerate(lengths):
    for j in range(nSims):
        print(f"Processing {i}, number {j}.")
        print(f"{(i*40+j)/(6*40)*100:.2f}% done.")

        t1 = time.time()
        randomString = "".join([str(r) for r in np.random.randint(0, 2, size=length)])
        #randomString = "".join([str(secrets.randbelow(2)) for i in range(lengths[i])])
        t2 = time.time()
        print(f"It took me {t2-t1:.2f}s to generate random string of size {length}.")

        t1 = time.time()
        bites = bitstring_to_bytes_compact(randomString)
        t2 = time.time()
        print(f"It took me {t2-t1:.2f}s to convert to a bytes object.")

        t1 = time.time()
        write_to_file_bytes_object(
            bites,
            "Experiments/3particlestrings/Graeme_randombites{}_{}".format(
                str(int(sizes[i])), str(j)
            ),
        )
        t2 = time.time()
        print(f"It took me {t2-t1:.2f}s to write down a bites object.")

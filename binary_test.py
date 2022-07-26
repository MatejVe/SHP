from sys import getsizeof
import zlib
import random


def int_to_bytes(input_int):
    isinstance(input_int, int) or exit(99)
    (input_int >= 0) or exit(98)
    if input_int == 0:
        return bytes([0])
    L1 = []

    num_bits = input_int.bit_length()

    while input_int:
        L1[0:0] = [(input_int & 0xFF)]
        input_int >>= 8

    if (num_bits % 8) == 0:
        L1[0:0] = [0]

    return bytes(L1)

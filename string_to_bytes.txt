# This algorithm converts an integer to a pure bytes object
# I found it online, I imagine a mistake could be hiding in here
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


# Actual conversion of the whole string to a bites object
def convert_to_bytes_object(string, bitsToBytes=8):
    """Only use on binary strings"""
    bites = b""
    i = 0
    while i < len(string) - bitsToBytes:
        bits = int_to_bytes(int(string[i : i + bitsToBytes], 2))
        i += bitsToBytes
        bites += bits

    if i != len(string):
        finalBits = int_to_bytes(int(string[i:], 2))
        bites += finalBits

    return bites
import numpy as np
import math
import sqlite3
import matplotlib.pyplot as plt


def convert_to_string_table(tableName):
    """Only use on tables that strictly contain collide indices."""
    collisions = []
    con = sqlite3.connect("Experiments.db")
    cur = con.cursor()

    for line in cur.execute("SELECT * FROM {}".format(tableName)):
        left, right = line[0][1:-1].split(", ")
        left = int(left) + 3 if int(left) < 0 else int(left)
        right = int(right) + 3 if int(right) < 0 else int(right)
        collisions.append((left, right))

    string = ""
    crnt = collisions[0]
    for i in range(1, len(collisions)):
        next = collisions[i]

        # If the next particles to collide are 'to the left' encode 0
        # If the next particles to collide are 'to the right' encode 1
        if crnt[0] == next[1]:
            string += "0"
        elif crnt[1] == next[0]:
            string += "1"

        crnt = next
    return string

def convert_to_string_file(filepath):
    f = open(filepath)
    collisions = []
    f.readline()
    f.readline()
    for line in f.readlines():
        left, right = line.strip().split(" ")
        left = int(left) + 3 if int(left) < 0 else int(left)
        right = int(right) + 3 if int(right) < 0 else int(right)
        collisions.append((left, right))
    
    string = ""
    crnt = collisions[0]
    for i in range(1, len(collisions)):
        next = collisions[i]
        # If the next particles to collide are 'to the left' encode 0
        # If the next particles to collide are 'to the right' encode 1
        if crnt[0] == next[1]:
            string += "0"
        elif crnt[1] == next[0]:
            string += "1"
        crnt = next
    return string


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


def jacknife_error(data):
    mean = np.mean(data)
    errors = []

    for i in range(len(data)):
        newData = data[:i] + data[i + 1 :]
        newMean = np.mean(newData)

        errors.append((newMean - mean) ** 2)

    error = np.sqrt(np.sum(errors))
    return error


def runsTest(string):
    runs, n1, n2 = 0, 0, 0

    for i in range(1, len(string)):
        if (string[i] == "1" and string[i - 1] == "0") or (
            string[i] == "0" and string[i - 1] == "1"
        ):
            runs += 1

        if string[i] == "1":
            n1 += 1
        else:
            n2 += 1

    runs_exp = ((2 * n1 * n2) / (n1 + n2)) + 1
    stan_dev = math.sqrt(
        (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / (((n1 + n2) ** 2) * (n1 + n2 - 1))
    )

    try:
        z = (runs - runs_exp) / stan_dev
        return z
    except ZeroDivisionError:
        print(f"Division by zero, n1={n1}, n2={n2}.")


class RunLengthEncoder:

    """
    class containing 3 methods that can be used to return a run-length
    encoded string.
    """

    def encode_a(self, text):

        """
        Returns a run-length encoded string from an input string.
        Note: This function will not return the character count in the return
        string if only a single instance of the character is found.

        Args:
            text (str): A string to encode

        Returns:
            str: A run length encoded string

        Example:
            input: "aaabbcdddd"
            returns: "3a2bc4d"
        """

        count = 1
        previous = ""
        mapping = list()

        for character in text:
            if character != previous:
                if previous:
                    mapping.append((previous, count))
                count = 1
                previous = character
            else:
                count += 1
        else:
            mapping.append((character, count))

        result = ""

        for character, count in mapping:
            if count == 1:
                result += character
            else:
                result += str(count)
                result += character

        return result

    def encode_b(self, text):

        """
        Returns a run-length encoded string from an input string.

        Args:
            text (str): A string to encode

        Returns:
            str: A run length encoded string

        Example:
            input: "aaabbcdddd"
            returns: "3a2b1c4d"
        """

        count = 1
        previous = ""
        mapping = list()

        for character in text:
            if character != previous:
                if previous:
                    mapping.append((previous, count))
                count = 1
                previous = character
            else:
                count += 1
        else:
            mapping.append((character, count))

        result = ""

        for character, count in mapping:
            result += str(count)
            result += character

        return result

    def encode_c(self, text):

        """
        Returns a run-length encoded string from an input string.
        This method uses a list comprehension to build the return
        string.

        Args:
            text (str): A string to encode

        Returns:
            str: A run length encoded string

        Example:
            input: "aaabbcdddd"
            returns: "3a2b1c4d"
        """

        count = 1
        previous = ""
        mapping = list()

        for character in text:
            if character != previous:
                if previous:
                    mapping.append((previous, count))
                count = 1
                previous = character
            else:
                count += 1
        else:
            mapping.append((character, count))

        result = "".join(f"{str(count)}{character}" for character, count in mapping)

        return result


def entropy2(labels, base=None):
    """Computes entropy of label distribution."""

    n_labels = len(labels)

    if n_labels <= 1:
        return 0

    value, counts = np.unique(list(labels), return_counts=True)
    probs = counts / n_labels
    n_classes = np.count_nonzero(probs)

    if n_classes <= 1:
        return 0

    ent = 0.0

    # Compute entropy
    base = math.e if base is None else base
    for i in probs:
        ent -= i * math.log(i, base)

    return ent


def percentage_and_error(strings, compressed):
    """
    Specific array of strings, compare the unified_plot.py and the other
    custom created plots.
    """
    percentage = [
        [c / s for c, s in zip(cgroup, sgroup)]
        for cgroup, sgroup in zip(compressed, strings)
    ]
    perc_means = [np.mean(group) for group in percentage]
    perc_errs = [jacknife_error(group) for group in percentage]
    return perc_means, perc_errs


def comparative_barplot(
    datas: list,
    yerrs: list,
    labels: list,
    xticks: list,
    ylabel: str,
    xlabel: str,
    title: str,
    filepath: str,
):
    """_summary_

    Args:
        datas (list): _description_
        yerrs (list): _description_
        labels (list): _description_
        xticks (list): _description_
        ylabel (str): _description_
        xlabel (str): _description_
        title (str): _description_
        filepath (str): _description_
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    x = np.arange(len(xticks))
    width = 0.35
    nbars = len(datas)


    for i in range(2):
        rects = ax.bar(x - width / 2 + 2*i/nbars*width, datas[i], width, yerr=yerrs[i], label=labels[i])
        ax.bar_label(rects, padding=3)

    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_xticks(x, xticks)
    ax.legend()

    fig.tight_layout()
    plt.savefig(filepath)
    plt.close()

import numpy as np
import math
import sqlite3


def convert_to_string(tableName):
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

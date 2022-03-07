from decimal import DivisionByZero
import numpy as np
import math

def convert_to_string(filepath):
    """Only use on files that strictly contain collide indices."""
    f = open(filepath)
    collisions = []

    f.readline()
    f.readline()

    for line in f.readlines():
        left, right = line.strip().split(' ')
        left = int(left) + 3 if int(left) < 0 else int(left)
        right = int(right) + 3 if int(right) < 0 else int(right)
        collisions.append((left, right))

    string = ''
    crnt = collisions[0]
    for i in range(1, len(collisions)):
        next = collisions[i]

        # If the next particles to collide are 'to the left' encode 0
        # If the next particles to collide are 'to the right' encode 1
        if crnt[0] == next[1]:
            string += '0'
        elif crnt[1] == next[0]:
            string += '1'

        crnt = next
    return string

def jacknife_error(data):
    mean = np.mean(data)
    errors = []

    for i in range(len(data)):
        newData = data[:i] + data[i+1:]
        newMean = np.mean(newData)

        errors.append((newMean - mean)**2)
        
    error = np.sqrt(np.sum(errors))
    return error

def runsTest(string):
    runs, n1, n2 = 0, 0, 0

    for i in range(1, len(string)):
        if (string[i] == '1' and string[i-1] == '0') or \
            (string[i] == '0' and string[i-1] == '1'):
            runs += 1

        if string[i] == '1':
            n1 += 1
        else:
            n2 += 1

    runs_exp = ((2*n1*n2)/(n1+n2))+1
    stan_dev = math.sqrt((2*n1*n2*(2*n1*n2-n1-n2))/ \
                       (((n1+n2)**2)*(n1+n2-1)))
    
    try:
        z = (runs-runs_exp)/stan_dev
        return z
    except ZeroDivisionError:
        print(f'Division by zero, n1={n1}, n2={n2}.')
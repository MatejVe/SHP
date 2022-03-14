import numpy as np

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

#print(convert_to_string('Experiments/runs_mass_tests1d/index0_0'))

#print(''.join([str(i) for i in np.random.randint(0, 2, size=10000)]))
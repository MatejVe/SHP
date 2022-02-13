import numpy as np
from decimal import Decimal


# Let's start with defining the classes that will be used in the simulation
# Base particle class
class Particle:
    """
    Base class for a particle. Not much is happening in here apart from storing
    the data for each particle and the update function which updates the data.
    """

    def __init__(self, mass, initPos, initVel, index=None):
        """"
        Arguments:
            mass (float) -> mass of the particle
            initPos (float) -> between 0 and 1, initial position of the particle
            initVel (float) -> pretty much any real number, initial velocity of the particle
            index (number) -> number assigned to this particle, defaults to None
        """
        self.mass = Decimal(str(mass))
        self.position = Decimal(str(initPos))
        self.velocity = Decimal(str(initVel))
        self.index = index

    def update(self, newPos=None, newVel=None):
        if newPos is not None:
            self.position = newPos

        if newVel is not None:
            self.velocity = newVel



# Auxiliary functions used in the code
def ring_distance(particle1, particle2):  # Assume that the particle1 is the first one to the left of the particle2
    pos1, vel1 = particle1.position, particle1.velocity
    pos2, vel2 = particle2.position, particle2.velocity

    # Transfer into the inertial reference frame of particle 1
    velDiff = vel2 - vel1

    if velDiff < 0:  # The right particle is moving towards the left one
        # Find the right (from particle 1) distance between the particles
        if pos2 > pos1:
            return abs(pos2 - pos1)
        elif pos2 < pos1: # e.g. x_1 = 0.9, x_2 = 0.2
            return Decimal("1") - abs(pos2 - pos1)
        else:
            return Decimal("1")
    elif velDiff > 0:
        # Find the left (from particle 1) distance between the particles
        if pos2 > pos1:
            return Decimal("1") - abs(pos2 - pos1)
        elif pos2 < pos1:
            return abs(pos2 - pos1)
        else:
            return Decimal("1")


def elastic_collision(M1, u1, M2, u2):
    v1 = (M1 - M2)/(M1 + M2) * u1 + 2*M2/(M1 + M2) * u2
    v2 = 2*M1/(M1+M2) * u1 + (M2 - M1)/(M1 + M2) * u2
    return v1, v2


def can_collide(particlel, particler):
    vell, indexl = particlel.velocity, particlel.index
    velr, indexr = particler.velocity, particler.index
    veldif = velr - vell
    indexdif = indexr - indexl
    if veldif > 0 and indexdif < 0:
        return False
    elif veldif < 0 and indexdif < 0:
        return True
    elif veldif > 0 and indexdif > 0:
        return False
    elif veldif < 0 and indexdif > 0:
        return True


def n3_check_for_undetected_collision(collisionIndices): # n3 stands for this only works for three particles
    if len(collisionIndices) == 2:
        collisionIndices.append(collisionIndices[0])



# Class that simulates a sistem of particlese and their interactions.
class Sistem:
    """
    Class which simulates a system of particles.
    """

    def __init__(self, particleNum, masses='random', initPositions='random', initVelocities='random'):
        """Sistem class which contains all the particles in the ring and their interactions.

        Args:
            particleNum (integer): Number of particles on the ring.
            masses (list, optional): List of masses for the particles. Must be in given in increasing positions of the particles. Defaults to 'random'.
            initPositions (list, optional): List of initial positions of the particles. Must be in increasing order. Defaults to 'random'.
            initVelocities (str, optional): List of initial velocities of the particles. Must be in increasing positions of the particles. Defaults to 'random'.

        Raises:
            Exception: Check if the masses input is correct.
            Exception: Check if the len of the masses list is the same as the number of particles.
            Exception: Check if the initPositions input is correct.
            Exception: Check if the len of the initPositions is the same as the number of particles.
            Exception: Check if the initVelocities input is correct.
            Exception: Check if the len of the initVelocities is the same as the number of particles.
        """
        self.particleNum = particleNum

        if masses == 'random':
            masses = np.random.random(size=particleNum) + 0.00001  # Adding a small constant to avoid assigning a mass of 0
        elif not isinstance(masses, list) and not isinstance(masses, np.ndarray):
            raise Exception('Not a valid input for the masses, if not "random" the input has to be a list of masses!')
        elif len(masses) != particleNum:
            raise Exception('Differing amount of masses to the amount of particles was provided!')

        if initPositions == 'random':
            initPositions = np.sort(np.random.random(size=particleNum))  # Sort the array so that the nearest neighbors of a particle i are always particles (i+1) and (i-1)
        elif not isinstance(initPositions, list) and not isinstance(initPositions, np.ndarray):
            raise Exception('Not a valid input for the masses, if no "random" the input has to be a list of positions!')
        elif len(initPositions) != particleNum:
            raise Exception('Differing amount of positions to the amount of particles was provided!')

        if initVelocities == 'random':
            initVelocities = 2*np.random.random(size=particleNum) - 1  # Initialize random velocities in the range [-1, 1)
        elif not isinstance(initVelocities, list) and not isinstance(initVelocities, np.ndarray):
            raise Exception('Not a valid input for the velocities, if not "random" the input has to be a list of velocities!')
        elif len(initVelocities) != particleNum:
            raise Exception('Differing amount of velocities to the amount of particles was provided!')

        self.particles = [Particle(mass, initPos, initVel, index) for index, (mass, initPos, initVel) in enumerate(zip(masses, initPositions, initVelocities))]
        self.positions = [particle.position for particle in self.particles]
        self.velocities = [particle.velocity for particle in self.particles]
        self.indexes = [particle.index for particle in self.particles]
        self.momentum = sum([particle.mass * particle.velocity for particle in self.particles])
        self.energy = sum([Decimal("0.5") * particle.mass * particle.velocity**2 for particle in self.particles])
        time, collidingParticles = self.find_next_event_s()
        self.time = time  # Store the time interval for which the particles are in the current state
        self.collideIndices = collidingParticles  # Store the indices of the two particles that will collide
        self.masses = masses


    def find_next_event_s(self):
        """
        Function that finds when the next collision will happen, and what two particles will collide.
        Returns a tuple of the format (time to collision, (index of particle 1 that collides, index of particle 2 that collides))
        """
        shortestTime = 1e10  # Start with a big number
        collideParticlesIndex = []
        for i in range(self.particleNum):
            if can_collide(self.particles[i-1], self.particles[i]):
                distanceLeft = ring_distance(self.particles[i-1], self.particles[i])  # Only check with the particle to the left, to avoid doublechecking

                if self.particles[i-1].velocity == self.particles[i].velocity:  # if the particles have the same velocity they will never collide
                    time = 1e10
                else:
                    time = distanceLeft / (abs(self.particles[i-1].velocity - self.particles[i].velocity))

                if time < shortestTime:
                    shortestTime = time
                    collideParticlesIndex = [(i-1, i)]
                elif time == shortestTime:
                    collideParticlesIndex.append((i-1, i))

        if self.particleNum == 3:  # Since it only works for 3 particles
            n3_check_for_undetected_collision(collideParticlesIndex)
        return (shortestTime, collideParticlesIndex)


    def update_particles(self, time, collidingIndices):
        """
        Function updates the positions of all particles and velocities of particles that collided in the event.
        """
        for particle in self.particles:
            # Update the positions of all the particles, the ones colliding will be at the same position
            vel = particle.velocity
            pos = particle.position
            newPos = (pos + time*vel) % 1
            if newPos < 0:
                newPos += Decimal("1")
            particle.update(newPos=newPos)
        

        for index in collidingIndices:
            left, right = index

            # Update the velocities of the particles that have collided
            mass1 = self.particles[left].mass
            vel1 = self.particles[left].velocity
            mass2 = self.particles[right].mass
            vel2 = self.particles[right].velocity

            newVel1, newVel2 = elastic_collision(mass1, vel1, mass2, vel2)

            self.particles[left].update(newVel=newVel1)
            self.particles[right].update(newVel=newVel2)

        # Recalculate the energy and momentum
        self.momentum = sum([particle.mass * particle.velocity for particle in self.particles])
        self.energy = sum([Decimal("0.5") * particle.mass * particle.velocity**2 for particle in self.particles])

        # Sort the particle list by their index
        self.particles.sort(key=lambda x: x.index)

        # Update the positions and velocities in the sistem class for purposes of logging them later
        self.positions = [particle.position for particle in self.particles]
        self.velocities = [particle.velocity for particle in self.particles]

        # Find the time the particles will stay in this state and the next two colliding particles
        time, colParIndex = self.find_next_event_s()
        self.time = time
        self.collideIndices = colParIndex


# Class wrapper for a single simulation experiment.
class Simulation:

    def __init__(self, collisionNumber, particleNumber, masses='random', initPoss='random', initVels='random'):
        """
        Simulation environment.

        Args:
            collisionNumber (int): Number of collisions to simulate.
            particleNumber ([type]): Number of particles to simulate.
            masses (list, optional): If a list is inputed make sure there is a mass for each particle. Defaults to 'random'.
            initPoss (list, optional): If a list is inputed make sure there is a position for each particle. Defaults to 'random'.
            initVels (list, optional): If a list is inputed make sure there is a velocity for each particle. Defaults to 'random'.
        """
        self.collisionNumber = collisionNumber
        self.sistem = Sistem(particleNum=particleNumber, masses=masses, initPositions=initPoss, initVelocities=initVels)


    def run(self, shouldPrint=None, shouldLog=None, filename=None):
        """
        This function collides the particles preset amount of times.

        Args:
            shouldPrint (list, optional): List of sistem object attributes you would like to have printed out. 
                                          Options are: 'positions', 'velocities', 'time', 'energy', 'momentum', 'indexes'.
                                          Defaults to None.
            shouldLog (list, optional): List of sistem object attributes you would like to have saved.
                                        Options are: 'positions', 'velocities', 'time', 'energy', 'momentum', 'indexes'.
                                        Defaults to None.
            filename (string, optional): Path and the filename of where you want the shouldLog data saved. If using shouldLog
                                        argument please provide the path as well.
        """
        if filename is not None:
            f = open(filename, 'w')

            # Write down number of particles and their masses
            massStr = ' '.join(str(mass) for mass in self.sistem.masses)

            f.write(f'Number of particles is: {self.sistem.particleNum} | Masses: {massStr} \n')
            
            attributeStr = '|'.join(attribute for attribute in shouldLog)
            f.write(attributeStr + '\n')

        for _ in range(self.collisionNumber):
            
            if shouldPrint is not None:
                for attribute in shouldPrint:  # Just fancy pritting tools, not important to the physics
                    if hasattr(self.sistem, attribute):
                        values = getattr(self.sistem, attribute)
                        if isinstance(values, list):
                            print(attribute + ':', end=' ')
                            for value in values:
                                if isinstance(value, tuple):
                                    print(' '.join(str(item) for item in value), end=' ')
                                else:
                                    print(f'{value:.2f}', end=' ')
                            print('', end='| ')
                        else:
                            print(f'{attribute}:{getattr(self.sistem, attribute):.3f} |', end=' ')

            if shouldPrint is not None:
                print('')

            if filename is not None:
                for attribute in shouldLog:
                    if hasattr(self.sistem, attribute):
                        values = getattr(self.sistem, attribute)
                        if isinstance(values, list):
                            if isinstance(values[0], tuple):
                                for value in values:
                                    f.write(' '.join(str(item) for item in value))
                            else:
                                f.write(' '.join(str(value) for value in values) + '|')
                        else:
                            f.write(str(getattr(self.sistem, attribute)) + '|')
                f.write('\n')

            self.sistem.update_particles(self.sistem.time, self.sistem.collideIndices)

        if filename is not None:
            f.close()


if __name__ == "__main__":
    import time
    time1 = time.time()
    # Experiment1 = Simulation(collisionNumber=20, particleNumber=3, masses=[1, 1, 1], initPoss=[0.2, 0.5, 0.8], initVels=[1, 0, -1])
    # Experiment1 = Simulation(collisionNumber=10, particleNumber=4, masses=[1, 1, 1, 1], initPoss=[0.1, 0.4, 0.6, 0.9], initVels=[1, -1, 1, -1])
    Experiment1 = Simulation(collisionNumber=10, particleNumber=3)
    Experiment1.run(shouldPrint=['positions', 'velocities', 'collideIndices'])
    time2 = time.time()
    print(f'Elapsed time: {time2 - time1}s')
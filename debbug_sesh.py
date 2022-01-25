import numpy as np

# TODO: fix the problem of simultaneous collisiions of particles

def ring_distance(particle1, particle2):  # Assume that the particle1 is the first one to the left of the particle2
    pos1, vel1 = particle1.position, particle1.velocity
    pos2, vel2 = particle2.position, particle2.velocity

    # Tranfer into the inertial reference frame of particle 1
    velDiff = vel2 - vel1

    if velDiff < 0:  # The right particle is moving towards the left one
        # Find the right (from particle 1) distance between the particles
        if pos2 > pos1:
            return abs(pos2 - pos1)
        elif pos2 < pos1: # e.g. x_1 = 0.9, x_2 = 0.2
            return 1 - abs(pos2 - pos1)
        else:
            return 1
    elif velDiff > 0:
        # Find the left (from particle 1) distance between the particles
        if pos2 > pos1:
            return 1 - abs(pos2 - pos1)
        elif pos2 < pos1:
            return abs(pos2 - pos1)
        else:
            return 1
    
def elastic_collision(M1, u1, M2, u2):
    v1 = (M1 - M2)/(M1 + M2) * u1 + 2*M2/(M1 + M2) * u2
    v2 = 2*M1/(M1+M2) * u1 + (M2 - M1)/(M1 + M2) * u2
    return v1, v2

# Let's start with defining the classes that will be used in the simulation
class Particle:
    """
    Base class for a particle. Not much is happening in here apart from storing
    the data for each particle and the update function which updates the data.
    """

    def __init__(self, mass, initPos, initVel):
        """"
        Arguments:
            mass (float) -> mass of the particle
            initPos (float) -> between 0 and 1, initial position of the particle
            initVel (float) -> pretty much any real number, initial velocity of the particle
        """
        self.mass = mass
        self.position = initPos
        self.velocity = initVel

    def update(self, newPos=None, newVel=None):
        if newPos is not None:
            self.position = newPos

        if newVel is not None:
            self.velocity = newVel


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
        elif not isinstance(masses, list):
            raise Exception('Not a valid input for the masses, if not "random" the input has to be a list of masses!')
        elif len(masses) != particleNum:
            raise Exception('Differing amount of masses to the amount of particles was provided!')

        if initPositions == 'random':
            initPositions = np.sort(np.random.random(size=particleNum))  # Sort the array so that the nearest neighbors of a particle i are always particles (i+1) and (i-1)
        elif not isinstance(initPositions, list):
            raise Exception('Not a valid input for the masses, if no "random" the input has to be a list of positions!')
        elif len(initPositions) != particleNum:
            raise Exception('Differing amount of positions to the amount of particles was provided!')

        if initVelocities == 'random':
            initVelocities = np.random.random(size=particleNum)
        elif not isinstance(initVelocities, list):
            raise Exception('Not a valid input for the velocities, if not "random" the input has to be a list of velocities!')
        elif len(initVelocities) != particleNum:
            raise Exception('Differing amount of velocities to the amount of particles was provided!')

        self.particles = [Particle(mass, initPos, initVel) for mass, initPos, initVel in zip(masses, initPositions, initVelocities)]
        self.positions = [particle.position for particle in self.particles]
        self.velocities = [particle.velocity for particle in self.particles]
        self.momentum = sum([particle.mass * particle.velocity for particle in self.particles])
        self.energy = sum([1/2 * particle.mass * particle.velocity**2 for particle in self.particles])

    def find_next_event(self):
        """
        Function that finds when the next collision will happen, and what two particles will collide.
        Returns a tuple of the format (time to collision, (index of particle 1 that collides, index of particle 2 that collides))
        """
        shortestTime = 1e10  # Start with a big number
        for i in range(self.particleNum):
            distanceLeft = ring_distance(self.particles[i], self.particles[i-1])  # Only check with the particle to the right, to avoid doublechecking

            if self.particles[i-1].velocity == self.particles[i].velocity:  # if the particles have the same velocity they will never collide
                time = 1e10
            else:
                time = distanceLeft / (abs(self.particles[i-1].velocity - self.particles[i].velocity))

            if time < shortestTime:
                shortestTime = time
                collideParticlesIndex = (i-1, i)

        return (shortestTime, collideParticlesIndex)

    def update_particles(self):
        """
        Function finds when the next collision will happen and which particles collide.
        Then, it updates the positions and velocities of all particles.
        """
        time, colParIndex = self.find_next_event()
        self.time = time  # Store the time interval for which the particles were in the state previous to the one that will be calculated now
        for particle in self.particles:
            # Update the positions of all the particles, the ones colliding will be at the same position
            vel = particle.velocity
            pos = particle.position
            newPos = (pos + time*vel) % 1
            particle.update(newPos=newPos)

        # Update the velocities of the particles that have collided
        mass1 = self.particles[colParIndex[0]].mass
        vel1 = self.particles[colParIndex[0]].velocity
        mass2 = self.particles[colParIndex[1]].mass
        vel2 = self.particles[colParIndex[1]].velocity

        newVel1, newVel2 = elastic_collision(mass1, vel1, mass2, vel2)

        self.particles[colParIndex[0]].update(newVel=newVel1)
        self.particles[colParIndex[1]].update(newVel=newVel2)

        # Recalculate the energy and momentum
        self.momentum = sum([particle.mass * particle.velocity for particle in self.particles])
        self.energy = sum([1/2 * particle.mass * particle.velocity**2 for particle in self.particles])

        # Update the positions and velocities in the sistem class for purposes of logging them later
        self.positions = [particle.position for particle in self.particles]
        self.velocities = [particle.velocity for particle in self.particles]


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

    def run(self, shouldPrint=None):
        """
        This function collides the particles preset amount of times.

        Args:
            shouldPrint (list, optional): List of sistem object attributes you would like to have printed out. 
                                          Options are: 'positions', 'velocities', 'time', 'energy', 'momentum'.
                                          Defaults to None.
        """
        for i in range(self.collisionNumber):
            self.sistem.update_particles()

            for attribute in shouldPrint:  # Just fancy pritting tools, not important to the physics
                if hasattr(self.sistem, attribute):
                    values = getattr(self.sistem, attribute)
                    if isinstance(values, list):
                        print(attribute + ':', end=' ')
                        for value in values:
                            print(f'{value:.2f}', end=' ')
                        print('', end=' | ')
                    else:
                        print(f'{attribute}:{getattr(self.sistem, attribute):e} |', end=' ')

            if shouldPrint is not None:
                print('')
            

Experiment1 = Simulation(collisionNumber=100, particleNumber=3)
Experiment1.run(shouldPrint=['positions', 'velocities', 'time', 'energy', 'momentum'])
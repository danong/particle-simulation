"""An n-Particle Simulation using Lennard-Jones potential.

We simulate n (up to ~200 on my computer) particles which repel each other when close to each other and attract when far
from each other. For each particle, we calculate the LJ force it experiences from every other particle.

We sum all the force vectors to determine the overall force and use
that overall force vector calculate the new position, angle, and velocity of each particle. Once that calculation is
complete for all particles, the program renders the screen with the particles.

Sources:
LJ Potential
http://polymer.bu.edu/Wasser/robert/work/node8.html
PyGame Tutorial:
http://www.petercollingridge.co.uk/pygame-physics-simulation
"""
import pygame
import random
import math
import itertools

# environmental variables
background_color = (255, 255, 255)
(width, height) = (1900, 1000)
number_of_particles = 20
epsilon = 0.000000001
sigma = 300
particle_size = 10
speed_limit = 10
speed_multiplier = 10
kinetic_energy = 0
potential_energy = 0

# HELPER FUNCTIONS
def add_vector((angle1, length1), (angle2, length2)):
    """Return the resultant sum of two vectors
    Parameters:
        (angle1, length1): Angle and length of first vector
        (angle2, length2): Angle and length of second vector
    """
    x_component = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y_component = math.cos(angle1) * length1 + math.cos(angle2) * length2
    length = math.hypot(x_component, y_component)
    angle = 0.5 * math.pi - math.atan2(y_component, x_component)
    return angle, length

def find_angle(a, b):
    """Find angle between two particles
    Parameters:
        a (Particle): first particle
        b (Particle): second particle
    """
    return math.atan2((b.y-a.y), (b.x-a.x)) + math.pi/2

def lj_potential(epsilon, sigma, r):
    """Return the lj potential of two particles

    Parameters:
        epsilon: depth of the potential well
        sigma: finite distance at which the inter-particle potential is zero
        r: distance between the particles
    """
    return 4 * epsilon * ((sigma/r)**12 - (sigma/r)**6)


def lj_force(epsilon, sigma, r):
    """Return the lj force of two particles. This is the derivative of the LJ Potential with respect to r

    Parameters:
        epsilon: depth of the potential well
        sigma: finite distance at which the inter-particle potential is zero
        r: distance between the particles
    """
    return (-24 * epsilon) * (2 *(sigma**12 / r**13) -(sigma**6 / r**7))


def particle_distance(a, b):
    """Return the distance of two particles

    Parameters:
        a (Particle): first particle
        b (Particle): second particle
    """
    return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)


class Particle:
    """A simple representation of a particle.

    Attributes:
        x: current x position
        y: current y position
        size: radius
        color: color
        thickness: border thickness (0 for solid color)
        speed: rate at which particle moves
        angle: angle that particle moves
    """

    def __init__(self, (x, y), size):
        """Initialize a particle's position and size.

        Args:
            (x, y): Starting position
            size: size
        """
        self.x = x
        self.y = y
        self.size = size
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.thickness = 0
        self.speed = 0
        self.angle = 0

    def display(self):
        """Draws particle on screen."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, self.thickness)

    def bounce(self):
        """Detects if particle has moved beyond the boundary and fixes its position."""
        # fix x coordinate if x is beyond boundary
        while self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
        while self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle

        # fix y coordinate if y is beyond boundary
        while self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
        while self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle

    def move(self):
        """Update position given angle and speed."""
        self.x += math.sin(self.angle) * self.speed * speed_multiplier
        self.y -= math.cos(self.angle) * self.speed * speed_multiplier

if __name__ == '__main__':
    # create screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Particle Simulation')

    # create and populate a list of particles
    my_particles = []
    c = pygame.time.Clock()
    for n in range(number_of_particles):
        # randomize starting particle attributes for now
        size = particle_size
        x = random.randint(size, width-size)
        y = random.randint(size, height-size)

        particle = Particle((x, y), size)
        particle.speed = 0
        particle.angle = 0
        my_particles.append(particle)

    # render screen
    running = True
    while running:
        kinetic_energy = potential_energy = 0
        # allow program to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill screen with background color
        screen.fill(background_color)

        # calculate inter-particle forces
        for a, b in itertools.combinations(my_particles, 2):
            temp_lj_force = lj_force(epsilon, sigma, particle_distance(a, b))
            temp_angle = find_angle(a, b)
            (a.angle, a.speed) = add_vector((a.angle, a.speed), (temp_angle, temp_lj_force))
            (b.angle, b.speed) = add_vector((b.angle, b.speed), (temp_angle+math.pi, temp_lj_force))
            potential_energy += lj_potential(epsilon, sigma, particle_distance(a, b))

        # fill screen with updated particles
        for particle in my_particles:
            kinetic_energy += 0.5 * particle.speed**2
            particle.move()
            particle.bounce()
            particle.display()
        c.tick(120/speed_multiplier)
        pygame.display.flip()

        print("Total Energy: ", kinetic_energy+potential_energy)
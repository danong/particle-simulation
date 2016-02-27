"""An n-Particle Simulation using Lennard-Jones potential.

Source:
http://polymer.bu.edu/Wasser/robert/work/node8.html
"""
import pygame
import random
import math

# HELPER FUNCTIONS
def add_vector((angle1, length1), (angle2, length2)):
    """Return the resultant sum of two vectors"""
    x_component = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y_component = math.cos(angle1) * length1 + math.cos(angle2) * length2
    length = math.hypot(x_component, y_component)
    angle = 0.5 * math.pi - math.atan2(y_component, x_component)
    return angle, length


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
        self.color = (0, 0, 255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0

    def display(self):
        """Draws particle on screen."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, self.thickness)

    def bounce(self):
        """Detects if particle has moved beyond the boundary and fixes its position."""
        # fix x coordinate if x is beyond boundary
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle

        # fix y coordinate if y is beyond boundary
        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle

    def move(self):
        """Update position given angle and speed."""
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

# environmental variables
background_color = (255, 255, 255)
(width, height) = (1200, 800)
number_of_particles = 2
epsilon = 0.65
sigma = 0.3166

if __name__ == '__main__':
    # create screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Particle Simulation')

    # create and populate a list of particles
    my_particles = []

    for n in range(number_of_particles):
        # randomize starting particle attributes for now
        # size = random.randint(10, 20)
        # x = random.randint(size, width-size)
        # y = random.randint(size, height-size)

        # particle = Particle((x, y), size)
        # particle.speed = random.random()
        # particle.angle = random.uniform(0, math.pi*2)
        size = 10
        x = random.randint(size, width-size)
        y = random.randint(size, height-size)
        particle = Particle((x, y), size)
        particle.speed = 0.5
        particle.angle = random.uniform(0, math.pi*2)
        my_particles.append(particle)

    # render screen
    running = True
    while running:
        # allow program to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill screen with background color
        screen.fill(background_color)

        # fill screen with updated particles
        for particle in my_particles:
            particle.move()
            particle.bounce()
            particle.display()

        print("lj force: ", lj_force(epsilon, sigma, particle_distance(my_particles[0], my_particles[1])))

        pygame.display.flip()
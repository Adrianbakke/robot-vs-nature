import pygame
import numpy

class Sheep:
    def __init__(self,screen,radius):
        self.radius = radius
        self.x_pos = 1500 + self.radius
        self.y_pos = 583
        self.width = 120
        self.height = 95
        self.hit = False
        self.sheep_passed = False
        self.GREY = (163, 163, 163)
        self.screen = screen
        self.red_sheep = False
        self.rand1 = numpy.random.randint(-25,25)
        self.rand2 = numpy.random.randint(-25,25)
        self.rand3 = numpy.random.randint(-25,25)
        self.sheep_img = pygame.image.load("img/sheep_white.png").convert()
        self.sheep_img.set_colorkey(self.GREY)
       


    def display(self):
        return self.screen.blit(self.sheep_img,(self.x_pos, self.y_pos))

    def top(self):
        return self.y_pos

    def right_side(self):
        return self.x_pos + self.width - 5

    def bottom(self):
        return self.y_pos + self.height

    def left_side(self):
        return self.x_pos + 25

    def rad_start(self):
        return self.x_pos - self.radius

    def rad_end(self):
        return self.x_pos + self.width + self.radius

    def length(self):
        return abs(self.left_side() - self.right_side())

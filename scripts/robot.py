import pygame

class Robot:
    def __init__(self,screen):
        self.x_pos = 150
        self.y_pos = 550
        self.width = 100
        self.height = 135
        self.screen = screen
        self.WHITE = (255, 255, 255)
        self.images = [pygame.image.load("Robot_1.png"),pygame.image.load("Robot_2.png"),pygame.image.load("Robot_3.png")]
        self.img.set_colorkey(self.WHITE)
    
    def display(self):
        self.screen.blit(self.img,(self.x_pos, self.y_pos))

    def top(self):
        return self.y_pos

    def right_side(self):
        return self.x_pos + self.width

    def bottom(self):
        return self.y_pos + self.height

    def left_side(self):
        return self.x_pos



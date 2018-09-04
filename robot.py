import pygame

class Robot:
    def __init__(self,screen):
        self.x_pos = 150
        self.y_pos = 550
        self.width = 90
        self.height = 135
        self.screen = screen
    
    def display(self, image):
        self.screen.blit(image,(self.x_pos, self.y_pos))

    def top(self):
        return self.y_pos

    def right_side(self):
        return self.x_pos + self.width - 5

    def bottom(self):
        return self.y_pos + self.height

    def left_side(self):
        return self.x_pos + 25

    def length(self):
        return abs(self.left_side() - self.right_side())

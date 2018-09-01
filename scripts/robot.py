import pygame

class Robot:
    def __init__(self,screen):
        self.x_pos = 150
        self.y_pos = 550
        self.width = 100
        self.height = 135
        self.screen = screen
        self.WHITE = (255, 255, 255)
        self.counter_for_img_switch = 0
        img1 = pygame.image.load("Robot_1.png")
        img1.set_colorkey(self.WHITE)
        img2 = pygame.image.load("Robot_2.png")
        img2.set_colorkey(self.WHITE)
        img3 = pygame.image.load("Robot_3.png")
        img3.set_colorkey(self.WHITE)
        img4 = pygame.image.load("Robot_4.png")
        img4.set_colorkey(self.WHITE)
        self.images = [img1, img3, img2, img3, img4]
    
    def display(self, xpos_background, robot_on_ground):
        self.screen.blit(self.running_robot(xpos_background, robot_on_ground),(self.x_pos, self.y_pos))

    def top(self):
        return self.y_pos

    def right_side(self):
        return self.x_pos + self.width

    def bottom(self):
        return self.y_pos + self.height

    def left_side(self):
        return self.x_pos

    def running_robot(self, xpos_background, robot_on_ground):
        if xpos_background % 30 == 0 and robot_on_ground:
            self.counter_for_img_switch = self.counter_for_img_switch + 1
            if self.counter_for_img_switch > 3:
                self.counter_for_img_switch = 0
        elif not robot_on_ground:
            self.counter_for_img_switch = 4

        image = self.images[self.counter_for_img_switch]
        return image



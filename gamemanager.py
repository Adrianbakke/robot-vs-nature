import pygame
import time
import numpy
from sheep import Sheep
from robot import Robot


class GameManager:
    def __init__(self):
        pygame.mixer.music.load("aud/cute.mp3")
        self.screen_width = 1200
        self.screen_height = 800
        self.screen_size = (self.screen_width,self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)
        background_image = pygame.image.load("img/game-background.jpg").convert_alpha()
        self.background_image = pygame.transform.scale(background_image, self.screen_size)
        self.xpos_background = 0
        self.jump = False
        self.jump_height = 0
        self.liv = 3
        self.lost_life = False
        self.start_score = 0
        self.sheeps = []
        self.BLACK = (0,0,0)
        self.speed = 15
        self.number_of_sheeps = 0
        self.img_robot = ["img/Robot_1.png", "img/Robot_3.png", "img/Robot_2.png", "img/Robot_3.png", "img/Robot_4.png"]
        self.img_sheep = ["img/sheep_white.png", 
                          "img/sheep_red.png"]
        self.GREY = (163, 163, 163)
        self.counter_for_img_switch = 0    
        self.start = True
        self.this_sheep = 0
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        self.myfont_menu = pygame.font.SysFont('Comic Sans MS', 72)
        self.myfont_menu2 = pygame.font.SysFont('Comic Sans MS', 80)
        self.height_advancement = 25
        self.gravity = 5
        self.height = (self.jump_height + 25) * 0.9
        self.get_robot_on_ground = False
        self.robot_on_ground = True
        self.jump_length = 0
        self.top_score = self.init_top_score()
        self.jm = Robot(self.screen)
        self.done = False
        self.slow = False
        self.start = True
        self.red_sheep = False
        self.red_sheep_start_pos = 0
        self.sound_effect_jump = pygame.mixer.Sound("aud/jump2.wav")
        self.sound_effect_jump.set_volume(0.2)
        self.sound_effect_sheep = pygame.mixer.Sound("aud/sheep.wav")
        self.sound_effect_sheep.set_volume(0.05)
        self.WHITE = (255, 255, 255)
    
    def hitbox_check(self, player_character, sheep_character):
        lengde_mann = player_character.width
        lengde_sheep = sheep_character.width
        lengde_rightMan_rightSheep = abs(player_character.right_side() - sheep_character.right_side())
        lengde_leftMan_leftSheep = abs(player_character.left_side() - sheep_character.left_side())
        bottom_man = player_character.bottom()
        top_sheep = sheep_character.top()

        if lengde_rightMan_rightSheep < lengde_sheep and lengde_leftMan_leftSheep < lengde_sheep and bottom_man > top_sheep and not self.jump and not sheep_character.hit:
                sheep_character.hit = True
                self.liv = self.liv - 1
                sheep_character.red_sheep = True
                sheep_character.sheep_img = pygame.image.load("img/sheep_red.png").convert()
                sheep_character.sheep_img.set_colorkey(self.GREY)
        
        if sheep_character.red_sheep and sheep_character.x_pos < 10:
            sheep_character.red_sheep = False
            sheep_character.sheep_img = pygame.image.load("img/sheep_white.png").convert()
            sheep_character.sheep_img.set_colorkey(self.GREY)

        if player_character.left_side() > sheep_character.right_side():
            sheep_character.hit = False

    def init_top_score(self, new_top_score=False, top_score=0):
        if new_top_score:
            top_score_file = open("top_score.txt", 'w')
            top_score_file.write('%d' % (top_score))
            top_score_file.close()

            top_score_file = open("top_score.txt", "r")
            content = top_score_file.readlines()
            top_score_file.close()

        else:
            try:
                top_score_file = open("top_score.txt", "r")
                content = top_score_file.readlines()
                top_score_file.close()
            except IOError:
                top_score_file = open("top_score.txt", 'w')
                top_score_file.write('0')
                top_score_file.close()

                top_score_file = open("top_score.txt", "r")
                content = top_score_file.readlines()
                top_score_file.close()

        return int(content[0])

    def jumperman(self,jumperman):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.robot_on_ground:
            self.jump = True
            self.start_pos = self.xpos_background
            self.robot_on_ground = False
            self.sound_effect_jump.play()

        if self.jump:
        ## jump_height increases by height_advancement which decrease by gravity = 5 every 30th pixel. This means that, since heigh_advancement initially is set to be 25px, that the if statement below has pass 5 times before the max jump height is reacht. That implies that the jump will be 25px + (30 * 5) = 175 px high.
            if round(self.jump_height+5)%30 == 0:
                self.height_advancement = self.height_advancement - self.gravity

            self.jump_height = self.jump_height + self.height_advancement
        
            if self.jump_height < 0:
                self.height_advancement = 25
                self.jump_height = 0
                self.robot_on_ground = True 
                self.jump = False

        jumperman.y_pos = 550 - self.jump_height

        jumperman.display(self.xpos_background, self.robot_on_ground) 

    def sheep_holder(self):
        score = self.start_score/10000000000
        if  round(score) > (100*self.number_of_sheeps) or \
            len(self.sheeps) == 0:            
                self.number_of_sheeps = self.number_of_sheeps + 1
                self.sheeps.append(["sheep_%d" % (self.number_of_sheeps)])
                self.sheeps[self.number_of_sheeps-1] = Sheep(self.screen)
                self.sound_effect_sheep.play()

        return self.sheeps

    def sheeps_on_screen(self, jumperman):
        player_character = jumperman
        for c,sheep in enumerate(self.sheep_holder()):
            random_number = numpy.random.randint(-10,10)
            
            if sheep.x_pos <= 0:
                sheep.x_pos = 2800 + (random_number * 100)

            else:  
                if sheep.x_pos >= self.sheeps[self.this_sheep].rad_start() \
                    and sheep.x_pos <= self.sheeps[self.this_sheep].rad_end() \
                    and sheep != self.sheeps[self.this_sheep]:
                    sheep.x_pos = + self.sheeps[self.this_sheep].rad_end() + 150 +(5*random_number)
                
                sheep.x_pos = sheep.x_pos - self.speed

                pygame.draw.line(self.screen, (5 + abs(sheep.rand1)*5, abs(sheep.rand2)*5,5 + abs(sheep.rand3*5)), (sheep.x_pos ,570), (sheep.x_pos+120,570), 10)

            if sheep.x_pos <= self.screen_width + 50:
                sheep.display()

            self.hitbox_check(player_character, sheep)

        if self.this_sheep == len(self.sheeps)-1:
            self.this_sheep = 0
        else:
            self.this_sheep = self.this_sheep + 1
        
    def life(self):
        score = self.start_score/10000000000
        if self.liv == 0:
            self.liv = 3
            self.number_of_sheeps = 0
            self.this_sheep = 0
            self.sheeps = []
            if self.top_score < score:
                self.top_score = self.init_top_score(True,score)
            self.start_score = 0
            pygame.mixer.music.rewind()

    def text(self):
        score = self.start_score/10000000000
        life = self.myfont.render('liv: %d' % (self.liv), False, (0, 0, 0))
        score = self.myfont.render('score: %d' % (score), False, (0, 0, 0))
        top_score_text = self.myfont.render('top-score: %d' % (self.top_score), False, (0, 0, 0))
    
        self.screen.blit(life,(self.screen_width/2,50))
        self.screen.blit(score,(self.screen_width/2,70))
        self.screen.blit(top_score_text,(self.screen_width/2,90))

    def background_logic(self):
        self.screen.blit(self.background_image, (self.xpos_background,0))
        self.screen.blit(self.background_image, (1200+self.xpos_background,0))
        if abs(self.xpos_background) >= self.screen_width:
            self.xpos_background = 0
        self.xpos_background = self.xpos_background-5

    def game(self):
        clock = pygame.time.Clock()
        pygame.mixer.music.play(-1)
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                    self.slow = True
            
            if self.slow:
                time.sleep(0.02)
            
            self.start_score = time.time() + self.start_score
            self.background_logic()
            self.jumperman(self.jm)
            self.sheeps_on_screen(self.jm)
            self.text()
            self.life()
            
            pygame.display.update()
            
            if self.start:
                time.sleep(2)
                self.start = False

            clock.tick(60)

    def cursor_over_object(self, x_pos, y_pos, width, height):
        return pygame.mouse.get_pos()[0] >= x_pos and \
               pygame.mouse.get_pos()[0] <= x_pos + width and \
               pygame.mouse.get_pos()[1] >= y_pos and \
               pygame.mouse.get_pos()[1] <= y_pos + height
    
    def start_screen(self):
        intro = True
        white = (255,255,255)
        color_change = False

        background_image = pygame.image.load("img/robot_vs_nature.png").convert_alpha()
        width = 150
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro =  False                
            
            self.screen.blit(background_image, (0,0))
            if color_change: 
                text =  self.myfont_menu2.render('PLAY', False, (255, 0, 0))
                text_width, text_height = self.myfont_menu2.size("PLAY")
            else:
                text =  self.myfont_menu.render('PLAY', False, (0, 0, 0))
                text_width, text_height = self.myfont_menu2.size("PLAY")
            
            self.screen.blit(text, (width,
                             self.screen_height/2))

            if self.cursor_over_object(width,
                             self.screen_height/2, text_width, text_height):
                color_change = True
            else:
                color_change = False
            
            if pygame.mouse.get_pressed()[0] == 1:
                if self.cursor_over_object(width,
                             self.screen_height/2, text_width, text_height):
                    print("success")
                    intro = False

            pygame.display.update()

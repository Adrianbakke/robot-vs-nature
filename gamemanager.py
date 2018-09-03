import pygame
import time
import numpy
from sheep import Sheep
from robot import Robot

class GameManager:
    def __init__(self):
        pygame.mixer.music.load("aud/elektro.mp3")
        self.screen_width = 1200
        self.screen_height = 800
        self.screen_size = (self.screen_width,self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)
        background_image = pygame.image.load("img/background3.jpg").convert()
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
        self.sound_effect_sheep.set_volume(0.15)
        self.WHITE = (255, 255, 255)
        self.sheep_passed_counter = 0
        self.next_level_jump_score = 50
        self.frame_counter = 0
        self.added_speed = 0
        img1 = pygame.image.load("img/Robot_1.png").convert()
        img1.set_colorkey(self.WHITE)
        img2 = pygame.image.load("img/Robot_2.png").convert() 
        img2.set_colorkey(self.WHITE)
        img3 = pygame.image.load("img/Robot_3.png").convert()
        img3.set_colorkey(self.WHITE)
        img4 = pygame.image.load("img/Robot_4.png").convert()
        img4.set_colorkey(self.WHITE)
        self.images = [img1, img3, img2, img3, img4]
        self.let_advancement_pass = True
        self.temp_speed_cont = 0
        self.img_rotation_tempo = 8
    
    def hitbox_check(self, player_character, sheep_character):
        lengde_mann = player_character.length()
        lengde_sheep = sheep_character.length()

        lengde_rightMan_rightSheep = abs(player_character.right_side() - sheep_character.right_side())
        lengde_leftMan_leftSheep = abs(player_character.left_side() - sheep_character.left_side())
        bottom_man = player_character.bottom()
        top_sheep = sheep_character.top()

        if  lengde_rightMan_rightSheep < lengde_sheep \
            and lengde_leftMan_leftSheep < lengde_sheep \
            and bottom_man > top_sheep \
            and not sheep_character.hit:
                sheep_character.hit = True
                sheep_character.sheep_passed = True
                self.liv = self.liv - 1
                sheep_character.red_sheep = True
                sheep_character.sheep_img = pygame.image.load("img/sheep_red.png").convert()
                sheep_character.sheep_img.set_colorkey(self.GREY)
        
        elif sheep_character.red_sheep \
             and sheep_character.x_pos < 10:
                sheep_character.red_sheep = False
                sheep_character.sheep_img = pygame.image.load("img/sheep_white.png").convert()
                sheep_character.sheep_img.set_colorkey(self.GREY)

        elif player_character.left_side() \
             > sheep_character.right_side() \
             and not sheep_character.sheep_passed :
                self.sheep_passed_counter += 1
                sheep_character.sheep_passed = True

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

    def running_robot(self, robot_on_ground, speed):
        images = self.images
        counter_for_img_switch = self.counter_for_img_switch
        frame_counter = self.frame_counter

        if frame_counter % self.img_rotation_tempo == 0 and robot_on_ground:
            frame_counter = 0
            counter_for_img_switch = counter_for_img_switch + 1
            if counter_for_img_switch > 3:
                counter_for_img_switch = 0
        elif not robot_on_ground:
            counter_for_img_switch = 4

        frame_counter += 1

        self.frame_counter = frame_counter
        self.counter_for_img_switch = counter_for_img_switch
        image = images[counter_for_img_switch]

        return image

    def robot_on_screen(self,robot):
        keys = pygame.key.get_pressed()
        xpos_background = self.xpos_background
        robot_on_ground = self.robot_on_ground
        speed = self.speed

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
        
            if self.jump_height <= 0:
                self.height_advancement = 25
                self.jump_height = 0
                self.robot_on_ground = True 
                self.jump = False

        robot.y_pos = 550 - self.jump_height

        robot_image = self.running_robot(robot_on_ground, speed)

        robot.display(robot_image)  

        # pygame.draw.line(self.screen, (0,0,0), (jumperman.left_side(),jumperman.y_pos), (jumperman.right_side(),jumperman.y_pos), 5)

        # pygame.draw.line(self.screen, (0,0,0), (jumperman.left_side(),jumperman.y_pos + jumperman.height), (jumperman.right_side(),jumperman.y_pos+ jumperman.height), 5)

        # pygame.draw.line(self.screen, (0,0,0), (jumperman.left_side(),jumperman.y_pos), (jumperman.left_side(),jumperman.y_pos + jumperman.height), 5)

        # pygame.draw.line(self.screen, (0,0,0), (jumperman.right_side(),jumperman.y_pos), (jumperman.right_side(),jumperman.y_pos + jumperman.height), 5)
    def score(self):
        return round(self.start_score/10000000000)

    def sheep_holder(self):
        score = self.start_score/10000000000
        if self.number_of_sheeps < 3: 
            if  round(score) > (100*self.number_of_sheeps) and round(score) <= 750 or \
                len(self.sheeps) == 0 or round(score) > (100*self.number_of_sheeps) + 750:            
                    self.number_of_sheeps = self.number_of_sheeps + 1
                    
                    if round(score) > 750:
                        self.sheeps.append(["sheep_%d" % (self.number_of_sheeps)])
                        self.sheeps[self.number_of_sheeps-1] = Sheep(self.screen,1300)
                        self.sound_effect_sheep.play()
                    else:
                        self.sheeps.append(["sheep_%d" % (self.number_of_sheeps)])
                        self.sheeps[self.number_of_sheeps-1] = Sheep(self.screen, 900)
                        self.sound_effect_sheep.play()

        return self.sheeps

    def sheeps_on_screen(self, jumperman):
        player_character = jumperman
        for c,sheep in enumerate(self.sheep_holder()):
            random_number = numpy.random.randint(-10,10)
            
            if sheep.x_pos <= 0:
                sheep.x_pos = 2500 + sheep.radius + (random_number * 100)
                sheep.sheep_passed = False
                if sheep.hit:
                    sheep.hit = False

            else:  
                if  sheep.x_pos >= self.sheeps[self.this_sheep].rad_start() \
                    and sheep.x_pos <= self.sheeps[self.this_sheep].rad_end() \
                    and sheep != self.sheeps[self.this_sheep]:
                        sheep.x_pos = self.sheeps[self.this_sheep].rad_end() + 150 +(5*random_number)
                
                sheep.x_pos = sheep.x_pos - self.speed

                # pygame.draw.line(self.screen, (5 + abs(sheep.rand1)*5, abs(sheep.rand2)*5,5 + abs(sheep.rand3*5)), (sheep.left_side(),sheep.y_pos), (sheep.right_side(),sheep.y_pos), 5)

                # pygame.draw.line(self.screen, (5 + abs(sheep.rand1)*5, abs(sheep.rand2)*5,5 + abs(sheep.rand3*5)), (sheep.left_side(),sheep.y_pos + sheep.height), (sheep.right_side(),sheep.y_pos + sheep.height), 5)

                # pygame.draw.line(self.screen, (5 + abs(sheep.rand1)*5, abs(sheep.rand2)*5,5 + abs(sheep.rand3*5)), (sheep.left_side(),sheep.y_pos), (sheep.left_side(),sheep.y_pos + sheep.height), 5)

                # pygame.draw.line(self.screen, (5 + abs(sheep.rand1)*5, abs(sheep.rand2)*5,5 + abs(sheep.rand3*5)), (sheep.right_side(),sheep.y_pos), (sheep.right_side(),sheep.y_pos + sheep.height), 5)

            if sheep.x_pos <= self.screen_width + 50:
                sheep.display()

            self.hitbox_check(player_character, sheep)

        if self.this_sheep == len(self.sheeps)-1:
            self.this_sheep = 0
        else:
            self.this_sheep += 1
        
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
            self.sheep_passed_counter = 0
            self.speed = 15
            pygame.mixer.music.rewind()

    def text(self):
        score = self.start_score/10000000000
        sheep_passed = self.myfont.render('jump-score: %d' % (self.sheep_passed_counter), False, (0, 0, 0))
        life = self.myfont.render('liv: %d' % (self.liv), False, (0, 0, 0))
        score_text = self.myfont.render('score: %d' % (score), False, (0, 0, 0))
        top_score_text = self.myfont.render('top-score: %d' % (self.top_score), False, (0, 0, 0))
    
        self.screen.blit(life,(self.screen_width/2,50))
        self.screen.blit(score_text,(self.screen_width/2,70))
        self.screen.blit(top_score_text,(self.screen_width/2,90))
        self.screen.blit(sheep_passed,(self.screen_width/2,110))

        if round(score) > 700 and round(score) < 755:
                text =  self.myfont_menu2.render('GET READY', False, (255, 0, 0))
                self.screen.blit(text, (self.screen_width/2 - 60,
                             self.screen_height/2 - 50))

    def background_logic(self):
        self.screen.blit(self.background_image, (self.xpos_background,0))
        self.screen.blit(self.background_image, (1200+self.xpos_background,0))
        
        if abs(self.xpos_background) >= self.screen_width:
            self.xpos_background = 0
        
        self.xpos_background = self.xpos_background-self.speed

    def advancement(self):
        score = self.score()

        if score == 750:
                self.this_sheep = 0
                self.number_of_sheeps = 0
                self.sheeps = []
                self.speed = 35

        if (score % 100) == 0 and self.let_advancement_pass and score > 0:
            self.speed += 2
            if self.img_rotation_tempo >= 1:
                self.img_rotation_tempo -= 1
            self.temp_speed_cont = round(score)
            self.let_advancement_pass = False

        elif not self.let_advancement_pass and (round(score) - self.temp_speed_cont) > 1:
            self.let_advancement_pass = True

    def game(self):
        clock = pygame.time.Clock()
        pygame.mixer.music.play(-1)
        score = self.start_score/10000000000
        
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                self.slow = True
            
            if self.slow:
                time.sleep(0.05)
            
            self.start_score = time.time() + self.start_score

            self.background_logic()
            self.robot_on_screen(self.jm)
            self.sheeps_on_screen(self.jm)
            self.text()
            self.life()
            self.advancement()

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

import math
import sys
import pygame
import os
import random

WIDTH = 623
HEIGHT = 150

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('DINO')

class Dino:
    def __init__(self):
        self.width = 44.0
        self.height = 44.0
        self.x = 10.0
        self.y = 80.0
        self.ground_height = 80.0
        self.jump_time = -1.0
        self.jump_duration = 1.0
        self.jump_interval = 0.05
        self.jump_height = 75.0
        self.on_ground = True
        self.jumping = False
        self.texture_num = 0
        self.set_texture()
        self.set_rect()
        self.set_sound()
        self.show()

    def update(self, delay):
        #jumping
        if self.jumping:
            if self.jump_time <= self.jump_duration:
                #calculate jump values
                time_elapsed = self.jump_time/self.jump_duration
                jump_frame = -1 * math.pow(time_elapsed, 2) + 1

                #apply jump values to y
                self.y = self.ground_height - (jump_frame * self.jump_height)
                self.rect.y = self.y

                #increment jump time
                self.jump_time += self.jump_interval
            else: 
                self.stop()
        #walking 
        elif self.on_ground and delay % 4 == 0:
            self.texture_num = (self.texture_num + 1) % 3
            self.set_texture()

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        path = os.path.join(f'assets/images/dino{self.texture_num}.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width/2, self.height/2)

    def set_sound(self):
        path = os.path.join('assets/sounds/jump.wav')
        self.sound = pygame.mixer.Sound(path)

    def jump(self):
        self.sound.play()
        self.jump_time = -1.0
        self.jumping = True
        self.on_ground = False

    def stop(self):
        self.jumping = False
        self.on_ground = True

class Cactus:
    def __init__(self, x):
        self.width = 34
        self.height = 44
        self.x = x
        self.y = 80
        self.set_texture()
        self.set_rect()
        self.show()
    
    def update(self, dx):
        self.x += dx
        self.rect.x = self.x

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        path = os.path.join('assets/images/cactus.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class Collision:
    def between(self, obj1, obj2):
        if obj1.rect.colliderect(obj2.rect):
            print(f"player x = {obj1.rect.x}")
            print(f"player y = {obj1.rect.y}")
            return True

class BG:
    def __init__(self, x):
        self.width = WIDTH
        self.height = HEIGHT
        self.x = x
        self.set_texture()
        self.show()

    def update(self, dx):
        self.x += dx
        if self.x <= -WIDTH:
            self.x = WIDTH

    def show(self):
        screen.blit(self.texture, (self.x, 0))

    def set_texture(self):
        path = os.path.join('assets/images/bg.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

class Score:
    def __init__(self, hs):
        self.high_score = hs
        self.score = 0
        self.font = pygame.font.SysFont('monospace', 18)
        self.color = (0, 0, 0)
        self.set_sound()
        self.show()

    def update(self, delay):
        self.score = delay // 10
        self.check_score()
        self.check_sound()

    def check_score(self):
        if self.score >= self.high_score:
            self.high_score = self.score

    def set_sound(self):
        path = os.path.join('assets/sounds/point.wav')
        self.sound = pygame.mixer.Sound(path)

    def show(self):
        self.label = self.font.render(f"HI {self.high_score} {self.score}", 1, self.color)
        label_width = self.label.get_rect().width
        screen.blit(self.label, (WIDTH - label_width - 10, 10))

    def check_sound(self):
        if self.score % 100 == 0 and self.score != 0:
            self.sound.play()

class Game:
    def __init__(self, high_score = 0):
        self.bg = [BG(0), BG(WIDTH)]
        self.dino = Dino()
        self.obstacles = []
        self.obstacle_dist = 84
        self.collision = Collision()
        self.score = Score(high_score)
        self.speed = 3
        self.is_playing = False
        self.is_over = False
        self.set_labels()
        self.set_sound()
        self.spawn_cactus()

    def set_labels(self):
        big_font = pygame.font.SysFont('monospace', 24, bold=True)
        small_font = pygame.font.SysFont('monospace', 18)
        self.big_label = big_font.render(f'G A M E O V E R', 1, (0, 0, 0))
        self.small_label = small_font.render(f'Press Space to Restart', 1, (0, 0, 0))
    
    def start(self):
        self.is_playing = True
        self.is_over = False

    def over(self):
        self.sound.play()
        screen.blit(self.big_label, (WIDTH // 2 - self.big_label.get_width() // 2, HEIGHT // 4))
        screen.blit(self.small_label, (WIDTH // 2 - self.small_label.get_width() // 2, HEIGHT // 2))
        self.is_playing = False
        self.is_over = True

    def can_spawn(self, delay):
        return delay % 100 == 0

    def spawn_cactus(self):
        #list with cactus
        if len(self.obstacles) > 0:
            prev_cactus = self.obstacles[-1]
            x = random.randint(prev_cactus.x + self.dino.width + self.obstacle_dist, 
                WIDTH + prev_cactus.x + self.dino.width + self.obstacle_dist)

        #empty
        else:
            x = random.randint(WIDTH + 100, 1000)

        #create new cactus
        cactus = Cactus(x)
        self.obstacles.append(cactus)

    def set_sound(self):
        path = os.path.join('assets/sounds/die.wav')
        self.sound = pygame.mixer.Sound(path)

    def restart(self):
        self.__init__(self.score.high_score)

def main():
    #objects
    game = Game()
    clock = pygame.time.Clock()
    dino = game.dino
    delay = 0

    while True:
        if game.is_playing:
            #delay update
            delay += 1

            #bg
            for bg in game.bg:
                bg.update(-game.speed)
                bg.show()
            
            #dino
            dino.update(delay)
            dino.show()

            #cactus
            if game.can_spawn(delay):
                game.spawn_cactus()

            for cactus in game.obstacles:
                cactus.update(-game.speed)
                cactus.show()

                #collision
                if game.collision.between(dino, cactus):
                    game.over()

            game.score.update(delay)
            game.score.show()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game.is_playing and game.is_over:
                        game.restart()
                        dino = game.dino
                        delay = 0
                    elif not game.is_playing and not game.is_over:
                        game.start()
                    
                    if game.is_playing and not game.is_over and dino.on_ground:
                        dino.jump()

        clock.tick(60)
        pygame.display.update()

main()
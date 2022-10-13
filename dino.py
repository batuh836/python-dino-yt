import math
import sys
import pygame
import os
import random

WIDTH = 623
HEIGHT = 150

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('DINO')

class Dino:
    def __init__(self):
        self.width = 44
        self.height = 44
        self.x = 10
        self.y = 80
        self.ground_height = 80
        self.texture_num = 0
        self.jump_time = -1.0
        self.jump_duration = 1.0
        self.jump_interval = 0.05
        self.jump_height = 75
        self.on_ground = True
        self.jumping = False
        self.set_texture()
        self.set_rect()
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
        self.rect = pygame.Rect(self.x, self.y, self.width * 0.75, self.height * 0.75)

    def jump(self):
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


class Game:
    def __init__(self):
        self.bg = [BG(0), BG(WIDTH)]
        self.dino = Dino()
        self.obstacles = []
        self.obstacle_dist = 84
        self.collision = Collision()
        self.speed = 3
        self.playing = False

    def start(self):
        self.playing = True

    def over(self):
        self.playing = False

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

def main():
    #objects
    game = Game()
    clock = pygame.time.Clock()
    dino = game.dino
    delay = 0

    while True:
        if game.playing:
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game.playing:
                        game.start()
                    if dino.on_ground:
                        dino.jump()

        clock.tick(60)
        pygame.display.update()

main()
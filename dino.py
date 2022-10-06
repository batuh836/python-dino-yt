import sys
import pygame
import os

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
        self.texture_num = 0
        self.dy = 4
        self.gravity = 1.2
        self.jump_height = 30
        self.ground_height = self.y
        self.on_ground = True
        self.jumping = False
        self.falling = False
        self.set_texture()
        self.show()

    def update(self, delay):
        #jumping
        if self.jumping:
            self.y -= self.dy
            if self.y <= self.jump_height:
                    self.fall()
        #falling
        elif self.falling:
            self.y += self.gravity * self.dy
            if self.y >= self.ground_height:
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

    def jump(self):
        self.jumping = True
        self.on_ground = False

    def fall(self):
        self.jumping = False
        self.falling = True

    def stop(self):
        self.falling = False
        self.on_ground = True


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
        self.speed = 3

def main():
    #objects
    game = Game()
    clock = pygame.time.Clock()
    dino = game.dino
    delay = 0

    while True:
        #delay update
        delay += 1

        #bg
        for bg in game.bg:
                bg.update(-game.speed)
                bg.show()
        
        #dino
        dino.update(delay)
        dino.show()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if dino.on_ground:
                        dino.jump()

        clock.tick(60)
        pygame.display.update()

main()
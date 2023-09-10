import pygame
from config import *
import math
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
        
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite
    
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x , y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TYLE_SIZE
        self.y = y * TYLE_SIZE
        self.width = TYLE_SIZE
        self.height = TYLE_SIZE
        
        self.x_change = 0
        self.y_change = 0
        
        self.facing = 'down'
        self.animation_loop = 1
         
        self.image = self.game.character_spritesheet.get_sprite(0, 0, TYLE_SIZE, TYLE_SIZE)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self):
        self.movement()
        self.animate()
        self.collie_enemy()
        
        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")
        self.x_change = 0
        self.y_change = 0
        
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
            
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
            
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
            
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
            
    def collie_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False
            
    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
                    self.rect.y = hits[0].rect.bottom
       
       
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
                    self.rect.y = hits[0].rect.bottom
                    
    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(0,0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(64,0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(128,0, self.width, self.height)]
        
        up_animations = [self.game.character_spritesheet.get_sprite(0,64, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(64,64, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(128,64, self.width, self.height)]
        
        left_animations = [self.game.character_spritesheet.get_sprite(0,128, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(64,128, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(128,128, self.width, self.height)]
        
        right_animations = [self.game.character_spritesheet.get_sprite(0,192, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(64, 192, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(128, 192, self.width, self.height)]
        
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0,0, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0,64, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
            
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0,128, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1  
            
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0,192, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TYLE_SIZE
        self.y = y * TYLE_SIZE
        self.width = TYLE_SIZE
        self.height = TYLE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['right', 'left'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemy_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'
    
    def animate(self):      
        left_animations = [self.game.enemy_spritesheet.get_sprite(0,128, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(64,128, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(128,128, self.width, self.height)]
        
        right_animations = [self.game.enemy_spritesheet.get_sprite(0,192, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(64, 192, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(128, 192, self.width, self.height)]
    
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(0,128, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1  
            
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(0,192, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

            
            
class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TYLE_SIZE
        self.y = y * TYLE_SIZE
        self.width = TYLE_SIZE
        self.height = TYLE_SIZE
        
        self.image = pygame.Surface([self.width, self.height])
        self.image = self.game.terrain_spritesheet.get_sprite(0,0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Celling(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TYLE_SIZE
        self.y = y * TYLE_SIZE
        self.width = TYLE_SIZE
        self.height = TYLE_SIZE
        
        self.image = pygame.Surface([self.width, self.height])
        self.image = self.game.celling_spritesheet.get_sprite(0,0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TYLE_SIZE
        self.y = y * TYLE_SIZE
        self.width = TYLE_SIZE
        self.height = TYLE_SIZE
        
        self.image = pygame.Surface([self.width, self.height])
        self.image = self.game.ground_spritesheet.get_sprite(0,0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class Button:
    def __init__(self, x, y):
        
        self.x = x
        self.y = y
        
        self.image = pygame.image.load('img/play_button.png')
        self.image =  pygame.transform.scale(self.image, (128, 64))
        
        self.rect = self.image.get_rect()
        
        self.button_width = self.image.get_width()
        self.button_height  = self.image.get_height()
        
        self.rect.x = self.x - (self.button_width /  2)
        self.rect.y = self.y + self.button_height
        
        self.image.blit(self.image, self.rect)
        
    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
    
class End_Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.SysFont('Arial', 32)
        self.content = content
        self.x = x
        self.y = y
        
        self.width = width
        self.height = height
        
        self.fg = fg
        self.bg = bg
        
        self.image  = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        
        self.button_width = self.image.get_width()
        self.button_height  = self.image.get_height()
        
        self.rect.x = self.x - (self.button_width / 2)
        self.rect.y = self.y + self.button_height
        
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center = (self.width /2, self.height/2))
        
        self.image.blit(self.text, self.text_rect)
        
    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
    
class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x  = x
        self.y = y
        self.width = TYLE_SIZE
        self.height = TYLE_SIZE
        
        self.animation_loop = 0
        
        self.image = self.game.attack_animation.get_sprite(0, 0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self):
        self.animate()
        self.collide()
        
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
        
    def animate(self, ):
        direction = self.game.player.facing
        down_animations = [self.game.attack_animation.get_sprite(0,64, self.width, self.height),
                           self.game.attack_animation.get_sprite(64,64, self.width, self.height),
                           self.game.attack_animation.get_sprite(128,64, self.width, self.height),
                           self.game.attack_animation.get_sprite(192,64, self.width, self.height),
                           self.game.attack_animation.get_sprite(256,64, self.width, self.height)]
        
        up_animations = [self.game.attack_animation.get_sprite(0,0, self.width, self.height),
                        self.game.attack_animation.get_sprite(64,0, self.width, self.height),
                        self.game.attack_animation.get_sprite(128,0, self.width, self.height),
                        self.game.attack_animation.get_sprite(192,0, self.width, self.height),
                        self.game.attack_animation.get_sprite(256,0, self.width, self.height)]
        
        left_animations = [self.game.attack_animation.get_sprite(0,192, self.width, self.height),
                           self.game.attack_animation.get_sprite(64,192, self.width, self.height),
                           self.game.attack_animation.get_sprite(128,192, self.width, self.height),
                           self.game.attack_animation.get_sprite(192,192, self.width, self.height),
                           self.game.attack_animation.get_sprite(256,192, self.width, self.height)]
        
        right_animations = [self.game.attack_animation.get_sprite(0,128, self.width, self.height),
                           self.game.attack_animation.get_sprite(64, 128, self.width, self.height),
                           self.game.attack_animation.get_sprite(128,128, self.width, self.height),
                           self.game.attack_animation.get_sprite(192,128, self.width, self.height),
                           self.game.attack_animation.get_sprite(256, 128, self.width, self.height)]
        
        if direction == "up":
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
                
        if direction == "down":
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        
        if direction == "right":
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
                
        if direction == "left":
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
                

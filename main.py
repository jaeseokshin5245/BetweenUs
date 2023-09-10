import pygame
from sprites import *
from config import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont('Arial', 32)
        
        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.ground_spritesheet = Spritesheet('img/ground.png')
        self.enemy_spritesheet = Spritesheet('img/enemy.png')
        self.intro_background = pygame.image.load('img/backimg.png')
        self.intro_title = pygame.image.load('img/intro_title.png')
        self.celling_spritesheet = Spritesheet('img/celling.png')
        self.end_background = pygame.image.load('img/end_background.jpg')
        self.attack_animation = Spritesheet('img/attack.png')
        
    def createTilemap(self):
        for i, row in enumerate(TILEMAP):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "C":
                    Celling(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates() 
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        
        self.createTilemap()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == "up":
                        Attack(self, self.player.rect.x, self.player.rect.y - TYLE_SIZE)
                    if self.player.facing == "down":
                        Attack(self, self.player.rect.x, self.player.rect.y + TYLE_SIZE)
                    if self.player.facing == "left":
                        Attack(self, self.player.rect.x - TYLE_SIZE, self.player.rect.y)
                    if self.player.facing == "right":
                        Attack(self, self.player.rect.x + TYLE_SIZE, self.player.rect.y)
                          
    def update(self):
        self.all_sprites.update()
        
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        
    def game_over(self):
        text = self.font.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
        
        restart_button = End_Button(WIN_WIDTH/2 , WIN_HEIGHT/2 + (WIN_HEIGHT/6), 120, 50, WHITE, BLACK, "RESTART", 32)
        
        for sprite in self.all_sprites:
            sprite.kill()
            
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()
                
            self.screen.blit(self.end_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
            
    def intro_screen(self):
        intro = True
        
        play_button = Button(int(WIN_WIDTH /2), int(WIN_HEIGHT /2))
        
        self.intro_title =  pygame.transform.scale(self.intro_title, (320, 160))
        self.title_width = self.intro_title.get_width()
        self.title_height = self.intro_title.get_height()
        
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(self.intro_title, (int((WIN_WIDTH /2) - (self.title_width /2)),int((WIN_HEIGHT /2) - (self.title_height))))
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
    
pygame.quit()
sys.exit()
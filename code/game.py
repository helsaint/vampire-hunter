import pygame
from player import Player
from settings import WINDOW_WIDTH,WINDOW_HEIGHT, TILE_SIZE
from sprites import *
from random import randint, choice
from pytmx.util_pygame import load_pygame
from groups import AllSprites, BulletSpriteGroup
from collision_handler import BulletEnemyCollision

class Game:
    def __init__(self):

        #Game Setup
        pygame.init()
        pygame.display.set_caption("Vampire Hunter")
        self.clock = pygame.time.Clock()

        #Surfaces
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

        #sprite groups
        self.all_sprites = AllSprites()
        self.bullet_sprites_group = BulletSpriteGroup()
        self.collision_sprites_group = pygame.sprite.Group()
        self.enemy_sprites_group = pygame.sprite.Group()

        #Enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_positions = []

        #Collisions
        self.bullet_enemy_collision =BulletEnemyCollision(self.bullet_sprites_group,
                                                          self.enemy_sprites_group, self.all_sprites)

        #Setup
        self.setup()
        
        #Main Game Loop
        self.running = True
        while self.running:
            dt = self.clock.tick()/1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == self.enemy_event:
                    enemy = EnemySprite(self.all_sprites,self.enemy_sprites_group,
                                        self.collision_sprites_group,
                                        self.player, choice(self.spawn_positions))

            self.display_surface.fill(color="black")
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.player.rect.center)
            self.bullet_enemy_collision.update()
            

            pygame.display.update()
        pygame.quit()

    def setup(self):
        # See
        map = load_pygame('./data/maps/world.tmx')
        for x,y,image in map.get_layer_by_name('Ground').tiles():
            GroundSprites(image, (TILE_SIZE*x, TILE_SIZE*y),
                          self.all_sprites)
            
        for obj in map.get_layer_by_name('Collisions'):
            temp_surface = pygame.Surface((obj.width, obj.height))
            CollisionSprites(temp_surface, (obj.x, obj.y),
                             self.collision_sprites_group)
            
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprites(obj.image,(obj.x,obj.y),
                              (self.all_sprites, self.collision_sprites_group))
            
        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player(self.all_sprites, self.collision_sprites_group,
                (obj.x, obj.y))
                self.gun = GunSprite(self.all_sprites, self.player, self.bullet_sprites_group)
            elif obj.name == 'Enemy':
                self.spawn_positions.append((obj.x,obj.y))
            
        

if __name__ == '__main__':
    new_game = Game()
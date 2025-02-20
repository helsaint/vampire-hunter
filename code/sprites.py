import pygame
from settings import SCALE_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, SCALE_BULLET, CHAMBER_TIME
from math import atan2, degrees
from groups import BulletSpriteGroup

class CollisionSprites(pygame.sprite.Sprite):
    def __init__(self, surface, position, group):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_frect(topleft=position)

class GroundSprites(pygame.sprite.Sprite):
    def __init__(self, surface, position, group):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_frect(topleft=position)
        self.is_background = True

class BulletSprite(pygame.sprite.Sprite):
    def __init__(self, all_sprites, position, direction):
        super().__init__(all_sprites)
        self.bullet_surface = pygame.transform.scale(
           pygame.image.load('./images/gun/bullet.png').convert_alpha(),
            (SCALE_BULLET,SCALE_BULLET))
        self.image = self.bullet_surface
        self.rect = self.image.get_frect(center=position)
        self.direction = direction
        self.lifespan = 3000
        self.creation_time = pygame.time.get_ticks()
        self.bullet_speed = 100

        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.bullet_lifetime()
        self.bullet_trajectory(dt)

    def bullet_lifetime(self):
        if (pygame.time.get_ticks() - self.creation_time > self.lifespan):
            self.kill()
    
    def bullet_trajectory(self, dt):
        self.rect.center += self.direction*self.bullet_speed * dt

class GunSprite(pygame.sprite.Sprite):
    def __init__(self, all_sprites, player, bullet_sprite_group):
        #player connection
        self.player = player
        self.distance = 40
        self.player_direction = pygame.Vector2(0,0)

        #setup
        super().__init__(all_sprites)
        self.all_sprites = all_sprites
        self.bullet_sprites_group = bullet_sprite_group
        self.gun_surface = pygame.transform.scale(
            pygame.image.load('./images/gun/gun.png').convert_alpha(),
            (SCALE_WIDTH,SCALE_WIDTH))
        self.image = self.gun_surface
        self.rect=self.image.get_frect(center=self.player.rect.center + 
                                       self.player_direction*self.distance)
        self.shoot_time = 0
        self.can_shoot = True
        
    def update(self, _):
        self.rect.center = self.player.rect.center + self.player_direction*self.distance
        self.rotate_gun()
        self.get_direction()
        self.shoot_gun()

    def chambered(self):
        if not(self.can_shoot):
            current_time = pygame.time.get_ticks()
            if(current_time - self.shoot_time > CHAMBER_TIME):
                self.can_shoot = True

    def get_direction(self):
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())
        player_position = pygame.Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.player_direction = (mouse_position - player_position).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surface, angle,1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surface, -angle,1)
            self.image = pygame.transform.flip(self.image, False, True)

    def shoot_gun(self):
        mouse_button = pygame.mouse.get_pressed()
        self.shot_time = pygame.time.get_ticks()
        if mouse_button[0] and self.can_shoot:
            start_position = self.rect.center + self.player_direction * 30
            bullet = BulletSprite(self.all_sprites,
                                   start_position, 
                                  self.player_direction)
            self.bullet_sprites_group.add(bullet)
            print(bullet)
            self.shoot_time = pygame.time.get_ticks()
        self.can_shoot = False

        self.chambered()

class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, all_sprites, enemy_sprite_group, collision_sprites, 
                 player, position):
        super().__init__(all_sprites)
        self.all_sprites = all_sprites
        self.add(enemy_sprite_group)
        self.add(collision_sprites)
        self.collision_sprites = collision_sprites
        self.player = player
        self.position = position

        #load enemy frames
        self.frames = self.load_images()
        self.frame_index = 0
        self.image = self.frames['bat'][self.frame_index].convert_alpha()
        self.rect = self.image.get_frect(center = position)
        self.hitbox_rect = self.rect.inflate(-20,-40)
        
        self.animation_speed = 6
        self.direction = pygame.Vector2(0,0)
        self.speed = 100

        self.mask = pygame.mask.from_surface(self.image)

    def load_images(self):
        enemy_list = ['bat', 'blob', 'skeleton']
        folders = ["./images/enemies/bat/","./images/enemies/blob/",
                   "./images/enemies/skeleton/"]
        number_frames = 4
        folders_dict = {}
        for i in range(len(enemy_list)):
            temp_list = []
            for j in range(number_frames):
                temp_image = pygame.image.load(folders[i] + f"{j}.png").convert_alpha()
                temp_list.append(temp_image)
            folders_dict[enemy_list[i]] = temp_list
        return folders_dict


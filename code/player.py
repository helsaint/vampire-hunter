import pygame
from settings import SCALE_WIDTH, SCALE_HEIGHT

class Player(pygame.sprite.Sprite):

    def __init__(self, all_sprites, collision_sprites,
                 position):
        super().__init__(all_sprites)
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.down_frames = [pygame.transform.scale(
            pygame.image.load(f"./images/player/down/{i}.png").convert_alpha(), (
                SCALE_WIDTH,SCALE_HEIGHT)) 
                            for i in range(4)]
        self.up_frames = [pygame.transform.scale(
            pygame.image.load(f"./images/player/up/{i}.png").convert_alpha(),
            (SCALE_WIDTH,SCALE_HEIGHT)) 
                            for i in range(4)]
        self.right_frames = [pygame.transform.scale(
            pygame.image.load(f"./images/player/right/{i}.png").convert_alpha(),
            (SCALE_WIDTH, SCALE_HEIGHT)) 
                            for i in range(4)]
        self.left_frames = [pygame.transform.scale(
            pygame.image.load(f"./images/player/left/{i}.png").convert_alpha(),
            (SCALE_WIDTH,SCALE_HEIGHT))
                            for i in range(4)]
        
        #initial position
        self.index = 0
        self.image = self.down_frames[self.index]
        self.rect = self.image.get_frect(center=position)
        self.hitbox_rect = self.rect.inflate(-40,-70)

        #movement
        self.speed = 300
        self.direction = pygame.Vector2(0,0)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        

    def move(self, dt):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_DOWN]):
            self.index += 20*dt
            self.image = self.down_frames[int(self.index)%4]
        if (keys[pygame.K_UP]):
            self.index += 20*dt
            self.image = self.up_frames[int(self.index)%4]
        if (keys[pygame.K_RIGHT]):
            self.index += 20*dt
            self.image = self.right_frames[int(self.index)%4]
        if (keys[pygame.K_LEFT]):
            self.index += 20*dt
            self.image = self.left_frames[int(self.index)%4]

        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")
        self.rect.center = self.hitbox_rect.center

    def update(self, dt):
        self.input()
        self.move(dt)

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if(direction == 'horizontal'):
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                if(direction == 'vertical'):
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
        
        
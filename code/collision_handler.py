import pygame

class BulletEnemyCollision:
    def __init__(self, bullet, enemy, all_sprites):
        self.bullet = bullet
        self.enemy = enemy
        self.all_sprites = all_sprites

    def update(self):
        bullet_hits = pygame.sprite.groupcollide(
            self.bullet, self.enemy, True, True, pygame.sprite.collide_mask)
        if(bullet_hits):
            print("Enemy Hit")

class BulletObjectCollision:
    def __init__(self, bullet, object):
        self.bullet = bullet
        self.object = object

    def update(self):
        bullet_hits = pygame.sprite.groupcollide(
            self.bullet, self.object, True, False, pygame.sprite.collide_mask
        )
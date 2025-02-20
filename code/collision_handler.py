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
            print(bullet_hits)
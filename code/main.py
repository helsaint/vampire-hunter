import pygame
from player import Player
from settings import WINDOW_WIDTH,WINDOW_HEIGHT
        

pygame.init()
pygame.display.set_caption("Vampire Hunter")

clock = pygame.time.Clock()

#Surfaces
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#Sprites
all_sprites = pygame.sprite.Group()

player = Player(all_sprites,
                (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
running = True
while running:
    dt = clock.tick()/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update(dt)

    display_surface.fill(color="black")

    all_sprites.draw(display_surface)

    pygame.display.update()
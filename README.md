game.py
- main code
- main game setup
- sprite groups; AllSprites, BulletSprtiteGroup, collision_sprites, enemy_sprites
- enemy event timer to spawn enemies
- game setup, load; tile map (GroundSprites),collision surfaces (ColissionSprites), Player and GunSprite

groups.py
- AllSprite class
    - draw sprites. Because sprites are drawn untop of each other we want the floor tiles to be drawn first
      then the rest. In the sprites.py the ground sprites have an attribute is_background = True
    - sprites are drawn with offsets to position them properly no matter the window dimensions
- BulletSpriteGroup. Currently just a placeholder class



import pygame

class LoadEnemyImages:
    def __init__(self):
        folders = ["./images/enemies/bat/","./images/enemies/blob/",
                   "./images/enemies/skeleton/"]
        enemy_list = ["bat", "blob", "skeleton"]
        number_frames = 4

        self.folders_dict = {}

        for i in range(len(folders)):
            temp_list = []
            for j in range(number_frames):
                temp_image = pygame.image.load(folders[i] + f"{j}.png").convert_alpha()
                temp_list.append(temp_image)
            self.folders_dict[enemy_list[i]] = temp_list
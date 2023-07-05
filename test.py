import pygame
import random

tiles_index = {}
tiles_index |= {0: [2, pygame.image.load("data/images/tiles/tile-0.png")]}
tiles_index |= {1: [4, pygame.image.load("data/images/tiles/tile-1.png")]}
tiles_index |= {2: [4, pygame.image.load("data/images/tiles/tile-2.png")]}
tiles_index |= {3: [2, pygame.image.load("data/images/tiles/tile-3.png")]}
tiles_index |= {4: [2, pygame.image.load("data/images/tiles/tile-4.png")]}
tiles_index |= {5: [2, pygame.image.load("data/images/tiles/tile-5.png")]}
# grass_img = pygame.image.load("data/images/grass.png")
# dirt_img = pygame.image.load("data/images/dirt.png")
# plant_img = pygame.image.load("data/images/plant.png").convert()
# for _, v in tiles_index.items():
#     print(v[1])

# for i in range(10):
#     current_trap = [0, 0, 0]
#     if random.randint(1, 2) == 2:
#         current_trap[0] = 1
#     else:
#         current_trap[1] = 1
#     if random.randint(1, 10) in [1, 2]:
#         current_trap[2] = 1

#     print(current_trap)
for i in range(20):
    print(random.choice([0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 5, 5]))

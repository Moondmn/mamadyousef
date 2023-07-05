import pygame, sys, os, random
import data.engine as e

clock = pygame.time.Clock()
framtime = 60
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()  # initiates pygame
pygame.mixer.set_num_channels(64)

pygame.display.set_caption("Pygame Platformer")

WINDOW_SIZE = (600, 400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window

display = pygame.Surface(
    (300, 200)
)  # used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

true_scroll = [0, 0]

CHUNK_SIZE = 12

obsticles = ("enemy", "spike", "steep")


def generate_chunk(cur_chunk_x):
    chunk_data = []
    current_mode = random.choice(obsticles)
    sides = ["r", "l"]
    # for y_pos in range(CHUNK_SIZE):
    # test = {"r": [[4, 3], 5, 4, 9], "l": [None, None, None, None]}
    #           "side" : hole, enemy, spike/saw, steep
    for x_pos in range(CHUNK_SIZE):
        # print(x_pos)
        target_x = cur_chunk_x * CHUNK_SIZE + x_pos

        enemy = 0
        # if cur_chunk_x > 5 and cur_chunk_x % 4 in [1, 3]:
        if current_mode == "enemy" and cur_chunk_x > 3:
            # if random.randint(1, 20) == 4:
            enemy = 1
        # print(cur_chunk_x)
        # target_y = y * CHUNK_SIZE + y_pos,
        jam = 0
        if current_mode == "spike":
            tile_type = 1
            # print("yes")
        else:
            tile_type = 2
        # if abs(target_x) == 50:
        #     jam = 1
        if tile_type != 0:
            # [[targetx, targety], ground, enemy, spike]
            chunk_data.append([[target_x, jam], tile_type, enemy])
    # print(chunk_data)
    # print(chunk_data, "\n")
    return chunk_data


class jumper_obj:
    def __init__(self, loc):
        self.loc = loc

    def render(self, surf, scroll):
        surf.blit(jumper_img, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], 8, 9)

    def collision_test(self, rect):
        jumper_rect = self.get_rect()
        return jumper_rect.colliderect(rect)


e.load_animations("data/images/entities/")

game_map = {}

grass_img = pygame.image.load("data/images/grass.png")
dirt_img = pygame.image.load("data/images/dirt.png")
plant_img = pygame.image.load("data/images/plant.png").convert()
plant_img.set_colorkey((255, 255, 255))

jumper_img = pygame.image.load("data/images/jumper.png").convert()
jumper_img.set_colorkey((255, 255, 255))

tile_index = {1: grass_img, 2: dirt_img, 3: plant_img}

jump_sound = pygame.mixer.Sound("data/audio/jump.wav")
grass_sounds = [
    pygame.mixer.Sound("data/audio/grass_0.wav"),
    pygame.mixer.Sound("data/audio/grass_1.wav"),
]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load("data/audio/music.wav")
pygame.mixer.music.play(-1)

grass_sound_timer = 0

player = e.entity(100, 100, 5, 13, "player")

enemies = []

# for i in range(5):
#     enemies.append([0, e.entity(random.randint(0, 600) - 300, 80, 13, 13, "enemy")])

# enemies.append([0, e.entity(600, 80, 13, 13, "enemy")])

background_objects = [
    [0.25, [120, 10, 70, 400]],
    [0.25, [280, 30, 40, 400]],
    [0.5, [30, 40, 40, 400]],
    [0.5, [130, 90, 100, 400]],
    [0.5, [300, 80, 120, 400]],
]

jumper_objects = []

for i in range(5):
    jumper_objects.append(jumper_obj((random.randint(0, 600) - 300, 80)))
sd = 0
while True:  # game loop
    display.fill((146, 244, 255))  # clear screen by filling it with blue

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    true_scroll[0] += player.x - true_scroll[0] - 152
    # true_scroll[1] += (player.y - true_scroll[1] - 106)
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    # scroll[1] = int(scroll[1])

    # pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))
    # for background_object in background_objects:
    #     obj_rect = pygame.Rect(
    #         background_object[1][0] - scroll[0] * background_object[0],
    #         background_object[1][1] - scroll[1] * background_object[0],
    #         background_object[1][2],
    #         background_object[1][3],
    #     )
    #     if background_object[0] == 0.5:
    #         pygame.draw.rect(display, (20, 170, 150), obj_rect)
    #     else:
    #         pygame.draw.rect(display, (15, 76, 73), obj_rect)
    ss = []
    tile_rects = []
    # for y in range(4):
    for x in range(4):
        target_x = x - 1 + int(round(scroll[0] / (CHUNK_SIZE * 16)))
        # target_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * 16)))
        target_chunk = str(target_x)
        if target_chunk not in game_map:
            game_map[target_chunk] = generate_chunk(target_x)
        # j = 0
        for tile in game_map[target_chunk]:
            i = 0
            display.blit(
                tile_index[tile[1]],
                (tile[0][0] * 16 - scroll[0], WINDOW_SIZE[1] - 216),
            )
            display.blit(
                tile_index[tile[1]],
                (0, tile[0][0] * 16 - scroll[0]),
            )
            if tile[2] == 1 and i == 0:
                # print("\nsuc\n")
                enemies.append([0, e.entity(tile[0][0] * 16, 80, 13, 13, "enemy")])
                i += 1
                tile[2] = 0
            # display.blit(
            #     pygame.transform.flip(tile_index[tile[1]], False, True),
            #     (tile[0][0] * 16 - scroll[0], tile[0][1] * 16 - scroll[1] - 200),
            # )
            if tile[1] in [1, 2]:
                # print(tile[1], scroll[0] // 16)
                tile_rects.append(
                    [
                        pygame.Rect(tile[0][0] * 16, WINDOW_SIZE[1] - 216, 16, 16),
                        tile[1],
                    ]
                )
                # tile_rects.append(
                #     pygame.Rect(tile[0][0] * 16, tile[0][1] * 16 - 200, 16, 16)
                # )

            # print(x)
            # if tile[1] in [3]:
            # print((tile[0][0] * 16 - scroll[0], tile[0][1] * 16 - scroll[1]))
    # for i in ss:
    #     enemies.append([0, e.entity(random.randint(0, 600) - 300, 80, 13, 13, "enemy")])
    player_movement = [0, 0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3
    # print(player_movement[1])
    if player_movement[1] < 0 or player_movement[1] == 3:
        # print(f"jump{sd}")
        player.set_action("idle")
        sd += 1
    if player_movement[0] == 0:
        player.set_action("idle")

    if player_movement[0] > 0 and player_movement[1] > 0 and player_movement[1] < 3:
        player.set_flip(False)
        # player.set_action("run")
        print(f"run{sd}")
    if player_movement[0] < 0:
        player.set_flip(True)
        player.set_action("run")

    # print(tile_rects)
    collision_types = player.move(player_movement, tile_rects)
    # if collision_types["data"][1][0] != "air":
    # print(collision_types["data"][1][2][1][1])

    if collision_types["bottom"] == True:
        air_timer = 0
        vertical_momentum = 0
        if player_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30
                random.choice(grass_sounds).play()
    else:
        air_timer += 1

    player.change_frame(1)
    player.display(display, scroll)

    # for jumper in jumper_objects:
    #     jumper.render(display, scroll)
    #     if jumper.collision_test(player.obj.rect):
    #         vertical_momentum = -8

    display_r = pygame.Rect(scroll[0], scroll[1], 300, 200)

    for i, enemy in enumerate(enemies):
        if display_r.colliderect(enemy[1].obj.rect):
            enemy[0] += 0.2
            if enemy[0] > 3:
                enemy[0] = 3
            enemy_movement = [0, enemy[0]]
            # if player.x > enemy[1].x + 5:
            #     enemy_movement[0] = 1
            # if player.x < enemy[1].x - 5:
            #     enemy_movement[0] = -1
            collision_types = enemy[1].move(enemy_movement, tile_rects)
            if collision_types["bottom"] == True:
                enemy[0] = 0
            if player.obj.rect.colliderect(enemy[1].obj.rect):
                # vertical_momentum = -4
                # print("damn")
                # enemy[1].y += 5
                # enemy_movement[1] -= 100
                enemies.pop(i)
            enemy[1].display(display, scroll)

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_w:
                pygame.mixer.music.fadeout(1000)
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    jump_sound.play()
                    vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)

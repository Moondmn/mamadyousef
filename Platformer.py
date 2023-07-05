import pygame, sys, os, random, secrets
import data.engine as e

clock = pygame.time.Clock()
framtime = 60
from pygame.locals import *

# pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()  # initiates pygame
pygame.mixer.set_num_channels(64)

pygame.display.set_caption("Pygame Platformer")

WINDOW_SIZE = (400, 600)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window

display = pygame.Surface(
    (200, 300)
)  # used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
vertical_momentum = 0
horizantal_momentum = 0
air_timer = 0

true_scroll = [0, 0]

CHUNK_SIZE = 12

# obsticles = ("enemy", "spike", "steep")


def switch(arg, var):
    x = 0
    for i in var:
        if arg == i:
            try:
                arg = var[x + 1]
            except IndexError:
                arg = var[x - 1]
            break
        x += 1
    return arg


side = "left"
touced_jumper = False
player_health = 5
is_dead = False
spike_cooldown = 0

trap = ["arrow", "spike", "hole"]


def generate_chunk(cur_chunk_y):
    chunk_data = []
    current_trap_r = [0, 0, 0]
    current_trap_l = [0, 0, 0]
    right = []
    left = []
    # for y_pos in range(CHUNK_SIZE):
    # test = {"r": [[4, 3], 5, 4, 9], "l": [None, None, None, None]}
    #           "side" : hole, enemy, spike/saw, steep
    if random.randint(1, 2) == 2:
        if random.randint(1, 2) == 0:
            current_trap_r[1] = 1
        else:
            current_trap_l[1] = 1
    elif random.randint(1, 2) == 2:
        if random.randint(1, 2) == 1:
            current_trap_l[0] = 1
        else:
            current_trap_r[0] = 1
    if (current_trap_r[0] == 1 or current_trap_r[1] == 1) and (
        current_trap_l[0] == 0 or current_trap_l[1] == 0
    ):
        if random.randint(1, 7) in [1, 3]:
            current_trap_l[2] = 1
    elif (current_trap_l[0] == 1 or current_trap_l[1] == 1) and (
        current_trap_r[0] == 0 or current_trap_r[1] == 0
    ):
        if random.randint(1, 6) in [1, 3]:
            current_trap_r[2] = 1
    if current_trap_l[2] == 0:
        if random.randint(1, 8) in [1, 3]:
            current_trap_l[2] = 1
    if current_trap_r[2] == 0:
        if random.randint(1, 6) in [1, 3]:
            current_trap_r[2] = 1
    # print("trap", current_trap_r, current_trap_l)
    position_trap = random.randint(2, 4)
    len_trap = random.randint(4, 7)
    # if :
    #     current_trap[3] = 1
    # if current_trap[0] ==1:
    target_y = cur_chunk_y * CHUNK_SIZE
    index = random.choice(tile_chance)
    if current_trap_r[1] == 1:
        for i in range(position_trap):
            right.append([i + target_y, "land", index])
        for i in range(len_trap):
            right.append([(i + position_trap) + target_y, "spike"])
        for i in range(CHUNK_SIZE - (len_trap + position_trap)):
            right.append([(i + position_trap + len_trap) + target_y, "land", index])

    if current_trap_l[1] == 1:
        for i in range(position_trap):
            left.append([i + target_y, "land", index])
        for i in range(len_trap):
            left.append([(i + position_trap) + target_y, "spike"])
        for i in range(CHUNK_SIZE - (len_trap + position_trap)):
            left.append([(i + position_trap + len_trap) + target_y, "land", index])

    if current_trap_r[0] == 1:
        for i in range(position_trap):
            right.append([i + target_y, "land", index])
        # for i in range(len_trap):
        right.append([(position_trap) + target_y, "arrow"])
        for i in range(CHUNK_SIZE - (position_trap + 1)):
            right.append([(i + position_trap + 1) + target_y, "land", index])

    if current_trap_l[0] == 1:
        for i in range(position_trap):
            left.append([i + target_y, "land", index])
        left.append([(position_trap) + target_y, "arrow"])
        for i in range(CHUNK_SIZE - (position_trap + 1)):
            left.append([(i + position_trap + 1) + target_y, "land", index])

    if current_trap_r[2] == 1:
        for i in range(position_trap):
            right.append([i + target_y, "land", index])
        for i in range(len_trap):
            right.append([(i + position_trap) + target_y, "hole"])
        for i in range(CHUNK_SIZE - (len_trap + position_trap)):
            right.append([(i + position_trap + len_trap) + target_y, "land", index])

    if current_trap_l[2] == 1:
        for i in range(position_trap):
            left.append([i + target_y, "land", index])
        for i in range(len_trap):
            left.append([(i + position_trap) + target_y, "hole"])
        for i in range(CHUNK_SIZE - (len_trap + position_trap)):
            left.append([(i + position_trap + len_trap) + target_y, "land", index])

    if current_trap_r == [0, 0, 0]:
        for i in range(CHUNK_SIZE):
            right.append([i + target_y, "land", index])
    if current_trap_l == [0, 0, 0]:
        for i in range(CHUNK_SIZE):
            left.append([i + target_y, "land", index])

    chunk_data.append([right, left])
    # print(chunk_data)
    # print(chunk_data, "\n")
    return [right, left]


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


# random.seed(random.choice(range(0, 100)))
e.load_animations("data/images/entities/")
tile_chance = [0, 1, 2, 3, 4, 0, 1, 2, 5, 1, 2, 3, 0, 1, 3]
game_map = {}
tiles_index = {}
tiles_index |= {0: pygame.image.load("data/images/tiles/tile-0.png").convert_alpha()}
tiles_index |= {1: pygame.image.load("data/images/tiles/tile-1.png").convert_alpha()}
tiles_index |= {2: pygame.image.load("data/images/tiles/tile-2.png").convert_alpha()}
tiles_index |= {3: pygame.image.load("data/images/tiles/tile-3.png").convert_alpha()}
tiles_index |= {4: pygame.image.load("data/images/tiles/tile-4.png").convert_alpha()}
tiles_index |= {5: pygame.image.load("data/images/tiles/tile-5.png").convert_alpha()}
for _, v in tiles_index.items():
    v.set_colorkey((255, 255, 255))
spike_img = pygame.image.load("data/images/traps/spike.png")
spike_img.set_colorkey((255, 255, 255))
shooter_img = pygame.image.load("data/images/traps/shooter.png")
shooter_img.set_colorkey((255, 255, 255))

heart = pygame.image.load("data/images/heart.png").convert()
heart.set_colorkey((255, 255, 255))
# dirt_img = pygame.image.load("data/images/dirt.png")
# plant_img = pygame.image.load("data/images/plant.png").convert()
# plant_img.set_colorkey((255, 255, 255))

jumper_img = pygame.image.load("data/images/jumper.png").convert()
jumper_img.set_colorkey((255, 255, 255))

# tile_index = {1: grass_img, 2: dirt_img, 3: plant_img}

# jump_sound = pygame.mixer.Sound("data/audio/jump.wav")


pygame.mixer.music.load("data/audio/music.wav")
pygame.mixer.music.play(-1)


player = e.entity(100, 100, 16, 18, "player")
# player.set_flip(False)
enemies = []
arrows = []
# for i in range(5):
#     enemies.append([0, e.entity(random.randint(0, 600) - 300, 80, 13, 13, "enemy")])

# enemies.append([0, e.entity(600, 80, 13, 13, "enemy")])


spike_collision = []
hole_collision = []
shooter_collision = []

jumper_objects = []

# for i in range(5):
#     jumper_objects.append(
#         jumper_obj(
#             (
#                 18,
#                 random.randint(0, 600) - 200,
#             )
#         )
#     )
sd = 0

while True:  # game loop
    display.fill((146, 244, 255))  # clear screen by filling it with blue

    true_scroll[1] += player.y - true_scroll[1] - 230
    # true_scroll[1] += (player.y - true_scroll[1] - 106)
    scroll = true_scroll.copy()
    scroll[1] = int(scroll[1])

    # ss = []
    tile_rects = []
    # mapc_r = []
    # mapc_l = []
    # for y in range(4):
    for y in range(3):
        target_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * 24)))
        # target_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * 16)))
        target_chunk = str(target_y)
        # genrate chunks if didnt exist ------------------
        if target_chunk not in game_map:
            game_map[target_chunk] = generate_chunk(target_y)
        # j = 0
        # print(target_chunk)
        # print(game_map[target_chunk][1], "\n\n\n")
        game_map_right = game_map[target_chunk][0]
        game_map_left = game_map[target_chunk][1]

        # print(index)

        i_r = 0
        i_l = 0
        s_r = 0
        s_l = 0
        sh_r = 0
        sh_l = 0
        # print(game_map_right)
        for mapr in game_map_right:
            print(mapr)
            if mapr[1] == "land":
                display.blit(
                    tiles_index[mapr[2]],
                    (200 - 24, mapr[0] * 24 - scroll[1]),
                )
                tile_rects.append(
                    [
                        pygame.Rect(200 - 24, mapr[0] * 24, 24, 24),
                        mapr[1],
                    ]
                )

            if mapr[1] == "spike":
                display.blit(
                    tiles_index[0],
                    (200 - 24, mapr[0] * 24 - scroll[1]),
                )
                display.blit(
                    spike_img,
                    (200 - 46, mapr[0] * 24 - scroll[1]),
                )
                # if s_r == 0:
                spike_collision.append(pygame.Rect(200 - 46, mapr[0] * 24, 30, 24))
                tile_rects.append(
                    [
                        pygame.Rect(200 - 24, mapr[0] * 24, 24, 24),
                        mapr[1],
                    ]
                )
            s_r += 1
            if mapr[1] == "arrow":
                display.blit(
                    shooter_img,
                    (200 - 24, mapr[0] * 24 - scroll[1]),
                )
                if sh_r == 0:
                    shooter_collision.append(
                        [
                            0,
                            e.entity(
                                200 - 37, mapr[0] * 24 - scroll[1], 13, 13, "shooter"
                            ),
                            "r",
                        ]
                    )
                tile_rects.append(
                    [
                        pygame.Rect(200 - 24, mapr[0] * 24, 24, 24),
                        mapr[1],
                    ]
                )
            sh_r = 1
            if mapr[1] == "hole":
                if i_r == 0:
                    if random.randint(1, 10) == 1:
                        jumper_objects.append(
                            jumper_obj(
                                (
                                    200 - 40,
                                    mapr[0] * 24 + 200,
                                )
                            )
                        )
                tile_rects.append(
                    [
                        pygame.Rect(200 - 3, mapr[0] * 24, 3, 24),
                        mapr[1],
                    ]
                )
                hole_collision.append(
                    pygame.Rect(200 - 24, mapr[0] * 24, 24, 24),
                )

                i_r += 1
        for mapl in game_map_left:
            if mapl[1] == "land":
                display.blit(
                    pygame.transform.flip(tiles_index[mapl[2]], True, False),
                    (0, mapl[0] * 24 - scroll[1]),
                )
                tile_rects.append(
                    [
                        pygame.Rect(0, mapl[0] * 24, 24, 24),
                        mapl[1],
                    ]
                )
            if mapl[1] == "spike":
                display.blit(
                    pygame.transform.flip(tiles_index[0], True, False),
                    (0, mapl[0] * 24 - scroll[1]),
                )
                display.blit(
                    pygame.transform.flip(spike_img, True, False),
                    (22, mapl[0] * 24 - scroll[1]),
                )
                # if s_l == 0:
                spike_collision.append(pygame.Rect(22, mapl[0] * 24, 30, 24))
                tile_rects.append(
                    [
                        pygame.Rect(0, mapl[0] * 24, 24, 24),
                        mapl[1],
                    ]
                )
            s_l += 1
            if mapl[1] == "arrow":
                display.blit(
                    pygame.transform.flip(shooter_img, True, False),
                    (0, mapl[0] * 24 - scroll[1]),
                )
                # shooter_collision.append(pygame.Rect(0, mapl[0] * 24, 240, 240))
                if sh_l == 1:
                    shooter_collision.append(
                        [
                            0,
                            e.entity(37, mapl[0] * 24 - scroll[1], 13, 13, "shooter"),
                            "l",
                        ]
                    )
                tile_rects.append(
                    [
                        pygame.Rect(0, mapl[0] * 24, 24, 24),
                        mapl[1],
                    ]
                )
            sh_l += 1

            if mapl[1] == "hole":
                if i_l == 0:
                    if random.randint(1, 10) == 1:
                        jumper_objects.append(
                            jumper_obj(
                                (
                                    28,
                                    mapl[0] * 24,
                                )
                            )
                        )
                tile_rects.append(
                    [
                        pygame.Rect(0, mapl[0] * 24, 3, 24),
                        mapr[1],
                    ]
                )
                hole_collision.append(
                    pygame.Rect(0, mapl[0] * 24, 24, 24),
                )
                i_l += 1
            if random.randint(1, 50000) in [
                1,
                6,
                7,
                30,
                24,
                123,
                156,
                56,
                18,
                34,
                86,
                95,
                75,
                3,
                43,
                355,
                1000,
                2000,
                3000,
            ]:
                enemies.append(
                    [
                        0,
                        e.entity(
                            random.randint(0, 350) - 156,
                            mapl[0] * 24 - 200,
                            13,
                            13,
                            "enemy",
                        ),
                    ]
                )

    # Player MOvement lol --------------------------------
    # todo should be rename after comp...
    player_movement = [0, 0]
    if moving_right == True:
        player_movement[1] -= 2
    # if moving_left == True:
    #     player_movement[1] -= 2

    # print(horizantal_momentum)
    if touced_jumper == True:
        player_movement[1] -= horizantal_momentum
        horizantal_momentum -= 0.2
    if horizantal_momentum < 0:
        # while horizantal_momentum != 0:
        #     horizantal_momentum -= 0.2
        horizantal_momentum = 0
        touced_jumper = False
        # if horizantal_momentum == 0:
        #     horizantal_momentum = 0

    if side == "left":
        # print(vertical_momentum)
        player_movement[0] -= vertical_momentum
        player.set_flip(True, True)
        # player.set_action("idle")
    elif side == "right":
        # player.set_action("idle")
        player_movement[0] += vertical_momentum
        player.set_flip(True, False)
        # player_movement[0] += 10
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3
    # print(player_movement[1])
    # if player_movement[1] < 0 or player_movement[1] == 3:
    #     # print(f"jump{sd}")
    #     player.set_action("idle")
    #     sd += 1
    # if player_movement[1] == 0:
    #     player.set_action("idle")

    if player_movement[1] > 0:  # and player_movement[1] > 0 and player_movement[1] < 3:
        player.set_flip(False, False)
        player.set_action("run")
        # print(f"run{sd}")/
    if player_movement[1] < 0:
        player.set_flip(True, False)
        player.set_action("run")
    if player.x > 100:
        player.set_flip(False, False)
    # print(tile_rects)
    collision_types = player.move(player_movement, tile_rects)
    # print(collision_types)
    # if collision_types["data"][1][0] != "air":
    # print(collision_types["data"][1][2][1][1])

    # if collision_types["bottom"] == True:
    #     air_timer = 0
    #     vertical_momentum = 0
    #     if player_movement[0] != 0:
    #         if grass_sound_timer == 0:
    #             grass_sound_timer = 30
    #             random.choice(grass_sounds).play()
    # else:
    #     air_timer += 1

    player.change_frame(1)
    player.display(display, scroll)

    for jumper in jumper_objects:
        jumper.render(display, scroll)
        if jumper.collision_test(player.obj.rect):
            # if side == "right":
            vertical_momentum = -3
            # elif side == "left":
            #     vertical_momentum = 8
            horizantal_momentum = 8
            touced_jumper = True

    if e.collision_test(player, spike_collision):
        player.set_action("jump")  # add damaged
        if spike_cooldown == 0:
            print("spiked - collided")
            spike_cooldown = 80
            player_health -= 1
            spike_collision.pop(0)
    if spike_cooldown > 0:
        spike_cooldown -= 0.5

    if e.collision_test(player, hole_collision):
        is_dead = True
        player_health = 0
        hole_collision.pop(0)
    # if e.collision_test(player, shooter_collision):
    #     print("shooter collided")
    #     shooter_collision.pop(0)

    display_r = pygame.Rect(scroll[0], scroll[1], 200, 300)
    display_s = pygame.Rect(scroll[0], scroll[1], 200, 300)
    for arrow in arrows:
        img = jumper_img.copy()
        arrow_movement = [0, 0]
        # print(arrow)
        if arrow[2] == "r":
            arrow_movement[0] += 3
            # arrow_movement[1] += 0.1
            arrow_obj = e.physics_obj(arrow[0], arrow[1], 10, 10)
        collisions = arrow_obj.move(arrow_movement, tile_rects)
        arrow[0] = arrow_obj.rect.x
        arrow[1] = arrow_obj.rect.y
        # print(arrow[0], arrow[1])
        # print(arrow)
        display.blit(
            img,
            (
                arrow[0],
                arrow[1] - scroll[1],
            ),
        )
        # try:
        #     arrows.remove(arrow)
        # except:
        #     pass
        # if collisions [2] ==True or collisions[3] == True:
        # print(collisions)
        # try:
        #     if abs(arrow[0] - (-ScrollY + DisplaySurf.get_width() / 2)) > 1000:
        #         Arrows.remove(Arrow)
        # except:
        #     pass
    for i, enemy in enumerate(enemies):
        if display_r.colliderect(enemy[1].obj.rect):
            # enemy[0] += 0.2
            # if enemy[0] > 3:
            #     enemy[0] = 3
            enemy_movement = [enemy[0], 0]
            if player.y - 30 > enemy[1].y + 5:
                enemy_movement[1] = 3
            if player.y + 30 < enemy[1].y - 5:
                enemy_movement[1] = -1.5

            if player.x > enemy[1].x + 5:
                enemy_movement[0] = 1
            if player.x < enemy[1].x - 5:
                enemy_movement[0] = -1.0
            collision_types = enemy[1].move(enemy_movement, tile_rects)
            if collision_types["left"] == True:
                enemy[0] = 0
            if player.obj.rect.colliderect(enemy[1].obj.rect):
                # pass
                # horizantal_momentum = -40
                player_health -= 1
                # print("damn")
                # enemy[1].y += 5
                # enemy_movement[1] -= 100
                enemies.pop(i)
                # arrows.append([enemy[1].x, enemy[1].y + 2, "r"])
            enemy[1].display(display, scroll)

    for i, enemy in enumerate(shooter_collision):
        # print(shooter)
        if display_s.colliderect(enemy[1].obj.rect):
            if enemy[2] == "l":
                enemy[0] += 0.2
                if enemy[0] > 3:
                    enemy[0] = 3
            elif enemy[2] == "r":
                enemy[0] -= 0.2
                if enemy[0] > 3:
                    enemy[0] = 3
            enemy_movement = [enemy[0], 0]

            collision_types = enemy[1].move(enemy_movement, tile_rects)
            if collision_types["left"] == True or collision_types["right"] == True:
                enemy[0] = 0
            if player.obj.rect.colliderect(enemy[1].obj.rect):
                arrows.append([enemy[1].x, enemy[1].y + 2, "r"])
                enemies.pop(i)
            enemy[1].display(display, scroll)
    if not is_dead:
        if player_health == 0:
            print("damn")
            exit()
        for i in range(player_health):
            display.blit(heart, (2 + i * 8, 2))
    if is_dead:
        print("complete - death")
        exit()
    moving_right = True
    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_i:
                side = switch(side, ["left", "right"])
                player.set_action("idle")
                # player.set_flip(True, False)
            if event.key == K_w:
                pygame.mixer.music.fadeout(1000)
            # if event.key == K_RIGHT:

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

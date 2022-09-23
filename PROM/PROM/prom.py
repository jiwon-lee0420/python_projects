import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

pygame.display.set_caption("First Game")

WINDOW_SIZE = (800,608)

win = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

surf = pygame.Surface((400, 304))

bg = pygame.image.load('background.png')

player_img = pygame.image.load('rachel_walk_1.png')
player_img_flipped = pygame.transform.flip(player_img, True, False)

present_img = pygame.image.load('present.png')

grass_topmid_img = pygame.image.load('grass_topmid.png')
grass_topleft_img = pygame.image.load('grass_topleft.png')
grass_topright_img = pygame.image.load('grass_topright.png')
grass_midleft_img = pygame.image.load('grass_midleft.png')
grass_mid_img = pygame.image.load('mid_tile.png')
grass_midright_img = pygame.image.load('grass_midright.png')
grass_bottomleft_img = pygame.image.load('grass_bottomleft.png')
grass_bottommid_img = pygame.image.load('grass_bottommid.png')
grass_bottomright_img = pygame.image.load('grass_bottomright.png')

TILE_SIZE = grass_mid_img.get_width()

class Presents():
    def __init__(self, loc):
        self.loc = loc

    def render(self, surf):
        surf.blit(present_img, (self.loc[0], self.loc[1]))

    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], 12, 12)

    def collide_test(self, rect):
        present_rect = self.get_rect()
        return present_rect.colliderect(rect)

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map('prom_lvl')

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):  # movement = [x,y]
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

def flipper(surf, counter):
    if counter < 1:
        surf = pygame.transform.flip(surf, True, False)
        counter += 1
        return surf, counter
    elif counter >= 1:
        return surf, counter

def animate(surf, path, counter, framerate):
    counter += framerate
    surf = pygame.image.load(path + str(int(counter)) + '.png')
    if counter >= 2:
        counter = 0
    return surf

def fade(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((255,255,255))
    for alpha in range(0,300):
        fade.set_alpha(alpha)
        win.blit(fade,(0,0))
        pygame.display.update()
        pygame.time.delay(5)

def won():
    while run:



        endgame_img = pygame.image.load('end_game_' + str(int(counter)) + '.png')
        surf.blit(endgame_img, (0,0))
        if counter >= 7:
            counter = counter
        else:
            counter += 0.01
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(60)

moving_right = False
moving_left = False

flip = False

player_y_momentum = 0
air_timer = 0

player_rect = pygame.Rect(50, 215, player_img.get_width(), player_img.get_height())

present_objects = []

p = Presents((375, 260))
r = Presents((380, 196))
o = Presents((5, 164))
m = Presents((10, 100))
question_mark = Presents((200, 52))

present_objects.append(p)
present_objects.append(r)
present_objects.append(o)
present_objects.append(m)
present_objects.append(question_mark)

counter = 0 #animation counter
score = 0

fade_bool = True
fade_counter = 0
end_img_counter = 0
while True:
    surf.blit(bg, (0,0))

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                surf.blit(grass_topleft_img, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                surf.blit(grass_topmid_img, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '3':
                surf.blit(grass_topright_img, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '4':
                surf.blit(grass_midleft_img, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '5':
                surf.blit(grass_mid_img, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '6':
                surf.blit(grass_midright_img, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '7':
                surf.blit(grass_bottomleft_img, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '8':
                surf.blit(grass_bottommid_img, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '9':
                surf.blit(grass_bottomright_img, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 5:
        player_y_momentum = 5

    if player_movement[0] == 0 and player_movement[1] == 0:
        player_img = animate(player_img, 'rachel_idle_', counter, 0.05)
    else:
        player_img = animate(player_img, 'rachel_walk_', counter, 0.01)

    if flip:
        surf.blit(player_img_flipped, (player_rect.x, player_rect.y))
    else:
        surf.blit(player_img, (player_rect.x, player_rect.y))

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1
    if collisions['top']:
        player_y_momentum += 1.5

    for present in present_objects:
        present.render(surf)
        if present.collide_test(player_rect):
            present_objects.remove(present)
            score += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if event.type == KEYDOWN:
        if event.key == K_RIGHT:
            moving_right = True
            flip = False
        if event.key == K_LEFT:
            moving_left = True
            flip = True
        if event.key == K_UP:
            if air_timer < 6:
                player_y_momentum = -5
    if event.type == KEYUP:
        if event.key == K_RIGHT:
            moving_right = False
        if event.key == K_LEFT:
            moving_left = False

    if score == 5:
        endgame_img = pygame.image.load('end_game_' + str(int(end_img_counter)) + '.png')
        endgame_img = pygame.transform.scale(endgame_img, (400, 304))
        surf.blit(endgame_img, (0,0))
        if end_img_counter >= 7:
            end_img_counter = end_img_counter
        else:
            end_img_counter += 0.01

    display = pygame.transform.scale(surf, WINDOW_SIZE)
    win.blit(display, (0, 0))
    pygame.display.update()
    clock.tick(60)

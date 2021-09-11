

import pathlib

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

from .map import Map
from .camera import Camera
from .anim import Animation


LEVEL = 1

def init_map():
    print('Loading level %d' % LEVEL)
    if LEVEL == 1:
        return Map.load(str(pathlib.Path(__file__).parent / 'levels/level1.npy'), 2, 2)
    elif LEVEL == 2:
        return Map.load(str(pathlib.Path(__file__).parent / 'levels/level2.npy'), 2, 2)
    else:
        assert False

def win(m):
    if LEVEL == 1:
        print('Nice! Now beat level 2 for the flag...')
    elif LEVEL == 2:
        print('Congrats! Here is your flag:')
        z = 0
        for i in range(48,-1,-1):
            z = (z * 3) + len(m.em.at((270*i)+129,8)) + len(m.em.at((270*i)+133,8))
        f = ''
        while z > 0:
            f = chr(z & 0x7f) + f
            z >>= 7
        print('flag{%s}' % f)
    else:
        assert False

def init(width, height):
    pygame.init()
    screen = pygame.display.set_mode([width, height], pygame.RESIZABLE)
    pygame.display.set_caption('Tur(n)ing Trees')
    return screen

def main():
    global LEVEL
    r = input('Select level [1,2]: ')
    if r.strip() == '1':
        LEVEL = 1
    elif r.strip() == '2':
        LEVEL = 2
    else:
        print('Invalid')
        exit(-1)

    m = init_map()

    width = 800
    height = 600
    screen = init(width, height)

    camera = Camera(2, 3, -4)

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60)

        # Check win condition (reach bottom right).
        if m.player.lx == m.width - 3 and m.player.ly == m.height - 3:
            win(m)
            exit(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    camera.zoom_out()
                elif event.key == pygame.K_e:
                    camera.zoom_in()
                elif event.key == pygame.K_r:
                    m = init_map()
                elif event.key == pygame.K_z:
                    if m.is_idle():
                        m.undo()
            
        keys = pygame.key.get_pressed()
        k_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        k_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        k_up = keys[pygame.K_UP] or keys[pygame.K_w]
        k_down = keys[pygame.K_DOWN] or keys[pygame.K_s]

        edt = dt
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            edt *= 30000

        if m.is_idle():
            if k_left: m.try_move(-1,0)
            elif k_right: m.try_move(1,0)
            elif k_up: m.try_move(0,-1)
            elif k_down: m.try_move(0,1)

        m.update(edt)
        camera.follow_player(m.player, dt)
        m.render(screen, camera)
        pygame.display.flip()

    pygame.quit()

if __name__=='__main__':
    main()

import pygame
from random import randrange
from time import sleep
from binascii import unhexlify

abc = b'4142434445464748494a4b4c4d4e4f505152535455565758595a6162636465666768696a6b6c6d6e6f707172737475767778797a31323' \
    b'3343536373839305f2d7b7d'
pygame.init()


class Game:
    def __init__(self, dW, dH, caption):
        self.dW = dW
        self.dH = dH
        self.alpha = abc
        self.hidden = b'666c61677b6a6b5f6e6f745f7468655f7265616c5f666c61677d'
        self.gD = pygame.display.set_mode((dW, dH))
        self.caption = caption
        self.clock = pygame.time.Clock()
        self.pause_text = ('Continue', 'Quit')
        self.font = 'rkill.ttf'
        self.text_small = 20
        self.text_large = 115


class Colors:
    def __init__(self):
        self.colors = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'block': (116, 77, 37),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'button': (130, 130, 130),
            'button_hover': (200, 200, 200),
            'button_click': (75, 75, 75),
            'bg': (0, 0, 126),
            'grey': (1, 1, 1)
        }


class Sprite:
    def __init__(self, img, imgL, imgR):
        self.img = pygame.image.load(img)
        self.imgL = pygame.image.load(imgL)
        self.imgR = pygame.image.load(imgR)


class Button:
    def __init__(self, text, color, color_hover, color_click, bX, bY, bW, bH, action=None):
        self.text = text
        self.color = color
        self.color_hover = color_hover
        self.color_click = color_click
        self.bX = bX
        self.bY = bY
        self.bW = bW
        self.bH = bH


class Enemy:
    def __init__(self, eX, speed, count):
        self.eX = eX
        self.eY = -600
        self.speed = speed
        self.eW = 100
        self.eH = 100
        self.count = count


class Msg:
    def __init__(self):
        self.alpha = b'4142434445464748494a4b4c4d4e4f505152535455565758595a6162636465666768696a6b6c6d6e6f70717273747' \
                b'5767778797a313233343536373839305f2d7b7d'

    def prnt(self, message):
        msg = str()
        for i in message:
            msg += u(self.alpha)[i]

        return msg


def u(n):
    return unhexlify(n).decode('utf-8')


def close_game():
    pygame.quit()
    quit()


def text_objects(text, font):
    text_surface = font.render(text, True, (255, 255, 255))
    return text_surface, text_surface.get_rect()


def draw_button(text, color, color_hover, color_click, bX, bY, bW, bH, action=None):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if (bX + bW) > mouse_pos[0] > bX and (bY + bH) > mouse_pos[1] > bY:
        pygame.draw.rect(gD, color_hover, (bX, bY, bW, bH))
        if mouse_click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(gD, color, (bX, bY, bW, bH))

    text_surf, text_rec = text_objects(text, pygame.font.Font(game.font, 20))
    text_rec.center = ((bX + (bW / 2)), (bY + (bH / 2)))
    gD.blit(text_surf, text_rec)


def escaped(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render(u(b'446f646765643a20') + str(count), True, color.colors['white'])
    gD.blit(text, (0, 0))


def show_msg(text):
    text_surf, text_rec = text_objects(text, pygame.font.Font(game.font, 115))
    text_rec.center = ((game.dW / 2), (game.dH / 2))
    gD.blit(text_surf, text_rec)

    pygame.display.update()

    sleep(2)
    gameloop()


def do_coll():
    show_msg(u(b'44656174682764'))


def check_border(cX, cY, cW, cH):
    if cX > game.dW - (cW / 2):
        return ((game.dW - (cW / 2)), cY)
    elif cX < 0 - (cX / 2):
        return ((0 - (cX / 2)), cY)

    if cY > game.dH - (cH / 1.5):
        return (cX, (game.dH - (cH / 1.5)))
    elif cY < 0 - (cH / 4):
        return (cX, (0 - (cH / 4)))


def get_intersect(x1, x2, w1, w2, y1, y2, h1):
    if y1 < (y2 + h1):
        if x1 > x2 and x1 < (x2 + w2) or (x1 + w1) > x2 and (x1 + w1) < (x2 + w2):
            do_coll()


def spawn_enemy(eX, eY):
    gD.blit(enemy.img, (eX, eY))


def spawn_player(pX, pY):
    gD.blit(player.img, (pX, pY))


def game_unpause():
    global pause
    pause = False


def game_pause():
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game.gD.fill((0, 0, 26))
        text_large = pygame.font.Font(game.font, 115)
        text_surf, text_rec = text_objects("Paused", text_large)
        text_rec.center = ((game.dW / 2), (game.dH / 2))
        gD.blit(text_surf, text_rec)

        draw_button(game.pause_text[0], color.colors['button'], color.colors['button_hover'],
                    color.colors['button_click'], (game.dW / 4 - 100), (game.dH / 1.25 - 25), 200, 50, game_unpause)
        draw_button(game.pause_text[1], color.colors['button'], color.colors['button_hover'],
                    color.colors['button_click'], (game.dW / 1.3 - 100), (game.dH / 1.25 - 25), 200, 50, close_game)

        pygame.display.update()
        game.clock.tick()


def set_pref():
    return str(f'{b.prnt([14, 5, 15, 15, 19])}')


def gs():
    gs_ = [64, 2, 26, 13, 19, 62, 28, 33, 54, 55, 45, 62, 29, 54, 55, 45, 33, 65]
    print(f"{set_pref()}{b.prnt(gs_)}")


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gD.fill(color.colors['bg'])
        font_sizes = {'large': 72, 'medium': 32}
        text_large = pygame.font.Font(game.font, font_sizes['large'])
        text_medium = pygame.font.Font(game.font, font_sizes['medium'])
        text_surf, text_rec = text_objects(game.caption, text_large)
        text_rec.center = ((game.dW / 2), (game.dH / 2))
        gD.blit(text_surf, text_rec)

        draw_button('GO!', color.colors['button'], color.colors['button_hover'], color.colors['button_click'],
                    (game.dW / 4 - 100), (game.dH / 1.25 - 25), 200, 50, gameloop)
        draw_button('Quit', color.colors['button'], color.colors['button_hover'], color.colors['button_click'],
                    (game.dW / 1.3 - 100), (game.dH / 1.25 - 25), 200, 50, close_game)

        pygame.display.update()
        game.clock.tick(15)


def gameloop():
    global pause
    x = game.dW * 0.45
    y = game.dH * 0.85
    xchange = 0
    ychange = 0

    enemy = Enemy(eX=randrange(0, game.dW), speed=4, count=1)
    gss, gf = 0, 0

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    game_pause()
                if event.key == pygame.K_LEFT:
                    xchange = -5
                elif event.key == pygame.K_RIGHT:
                    xchange = 5
                elif event.key == pygame.K_UP:
                    ychange = -2
                elif event.key == pygame.K_DOWN:
                    ychange = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    xchange = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    ychange = 0

        x += xchange
        y += ychange

        gD.fill(color.colors['bg'])
        spawn_enemy(enemy.eX, enemy.eY)
        enemy.eY += enemy.speed
        spawn_player(x, y)
        escaped(gss)

        if enemy.eY > game.dH:
            enemy.eY = 0 - enemy.eH
            enemy.eX = randrange(0, game.dW)
            gss += 0x1
            gf = gss
            enemy.speed += 1
            if gf > (5 * 20):
                gf = (25 * 4)
                game.pause_text = gs()
                pause = True

        if x > game.dW - (player.img.get_rect().size[0] / 2):
            x = game.dW - (player.img.get_rect().size[0] / 2)
        elif x < 0 - (player.img.get_rect().size[0] / 2):
            x = 0 - (player.img.get_rect().size[0] / 2)

        if y > game.dH - (player.img.get_rect().size[1] / 2):
            y = game.dH - (player.img.get_rect().size[1] / 2)
        elif y < 0 - (player.img.get_rect().size[1] / 4):
            y = 0 - (player.img.get_rect().size[1] / 4)

        get_intersect(x, enemy.eX, player.img.get_rect().size[0], enemy.eW, y, enemy.eY, enemy.eH)

        pygame.display.update()
        game.clock.tick(60)


# MAIN
b = Msg()
print(b.prnt([31, 37, 26, 32, 64]))

game = Game(dW=800, dH=600, caption='Trick or Treat')
player = Sprite('img/player.png', 'img/player.png', 'img/player.png')
enemy = Sprite('img/enemy.png', 'img/enemy.png', 'img/enemy.png')
pygame.display.set_caption(game.caption)
player_sprite = pygame.image.load('img/player.png')
pygame_gs = (game.dW, game.dH, player_sprite.get_rect().size[0], player_sprite.get_rect().size[1])
pause = True
a = u(abc)
gD = pygame.display.set_mode((game.dW, game.dH))
color = Colors()

game_intro()
gameloop()
pygame.quit()
quit()

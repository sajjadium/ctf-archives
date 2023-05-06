import pygame
import pyBaba
import config
import sys
import sprites

if len(sys.argv[1]) < 2:
    print('Usage: main.py [map]')
    sys.exit(1)

game = pyBaba.Game(sys.argv[1])
screen_size = (game.GetMap().GetWidth() * config.BLOCK_SIZE,
               game.GetMap().GetHeight() * config.BLOCK_SIZE)
screen = pygame.display.set_mode(
    (screen_size[0], screen_size[1]), pygame.DOUBLEBUF)
sprite_loader = sprites.SpriteLoader()

result_image = sprites.ResultImage()
result_image_group = pygame.sprite.Group()
result_image_group.add(result_image)


def draw_obj(x_pos, y_pos):
    objects = game.GetMap().At(x_pos, y_pos)

    for obj_type in objects.GetTypes():
        if pyBaba.IsTextType(obj_type):
            obj_image = sprite_loader.text_images[obj_type]
        else:
            if obj_type == pyBaba.ObjectType.ICON_EMPTY:
                continue
            obj_image = sprite_loader.icon_images[obj_type]
        obj_image.render(screen, (x_pos * config.BLOCK_SIZE,
                                  y_pos * config.BLOCK_SIZE))


def draw():
    for y_pos in range(game.GetMap().GetHeight()):
        for x_pos in range(game.GetMap().GetWidth()):
            draw_obj(x_pos, y_pos)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    clock = pygame.time.Clock()

    game_over = False

    while True:
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            if game.GetPlayState() == pyBaba.PlayState.WON:
                result_image_group.update(pyBaba.PlayState.WON, screen_size)
                result_image_group.draw(screen)
            else:
                result_image_group.update(pyBaba.PlayState.LOST, screen_size)
                result_image_group.draw(screen)
            pygame.display.flip()
            continue

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:
                    game.MovePlayer(pyBaba.Direction.UP)
                elif event.key == pygame.K_DOWN:
                    game.MovePlayer(pyBaba.Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    game.MovePlayer(pyBaba.Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    game.MovePlayer(pyBaba.Direction.RIGHT)
                elif event.key == pygame.K_x:
                    game.Undo()

        if game.GetPlayState() == pyBaba.PlayState.WON or game.GetPlayState() == pyBaba.PlayState.LOST:
            game_over = True

        screen.fill(config.COLOR_BACKGROUND)
        draw()
        pygame.display.flip()

        clock.tick(config.FPS)

import pygame
import pyBaba
from images import GIFImage


class SpriteLoader:
    def __init__(self):
        self.icon_images = {
            pyBaba.ObjectType.ICON_BABA:    'BABA',
            pyBaba.ObjectType.ICON_BRICK:   'BRICK',
            pyBaba.ObjectType.ICON_FLAG:    'FLAG',
            pyBaba.ObjectType.ICON_GRASS:   'GRASS',
            pyBaba.ObjectType.ICON_HEDGE:   'HEDGE',
            pyBaba.ObjectType.ICON_LAVA:    'LAVA',
            pyBaba.ObjectType.ICON_JIJI:    'JIJI',
            pyBaba.ObjectType.ICON_ROCK:    'ROCK',
            pyBaba.ObjectType.ICON_TILE:    'TILE',
            pyBaba.ObjectType.ICON_TREE:    'TREE',
            pyBaba.ObjectType.ICON_WALL:    'WALL',
            pyBaba.ObjectType.ICON_WATER:   'WATER',
        }

        for i in self.icon_images:
            self.icon_images[i] = GIFImage(
                './sprites/icon/{}.gif'.format(self.icon_images[i]))
            self.icon_images[i].scale(1.0)

        self.text_images = {
            # nonn type
            pyBaba.ObjectType.BABA:     'BABA',
            pyBaba.ObjectType.BRICK:    'BRICK',
            pyBaba.ObjectType.FLAG:     'FLAG',
            pyBaba.ObjectType.GRASS:    'GRASS',
            pyBaba.ObjectType.HEDGE:    'HEDGE',
            pyBaba.ObjectType.LAVA:     'LAVA',
            pyBaba.ObjectType.JIJI:     'JIJI',
            pyBaba.ObjectType.ROCK:     'ROCK',
            pyBaba.ObjectType.TEXT:     'TEXT',
            pyBaba.ObjectType.TILE:     'TILE',
            pyBaba.ObjectType.TREE:     'TREE',
            pyBaba.ObjectType.WALL:     'WALL',
            pyBaba.ObjectType.WATER:    'WATER',

            # op type
            pyBaba.ObjectType.HAS:      'HAS',
            pyBaba.ObjectType.IS:       'IS',
            pyBaba.ObjectType.AND:      'AND',
            pyBaba.ObjectType.NOT:      'NOT',

            # property type
            pyBaba.ObjectType.YOU:      'YOU',
            pyBaba.ObjectType.STOP:     'STOP',
            pyBaba.ObjectType.PUSH:     'PUSH',
            pyBaba.ObjectType.WIN:      'WIN',
            pyBaba.ObjectType.SINK:     'SINK',
            pyBaba.ObjectType.HOT:      'HOT',
            pyBaba.ObjectType.MELT:     'MELT',
            pyBaba.ObjectType.SHUT:     'SHUT',
            pyBaba.ObjectType.OPEN:     'OPEN',
        }

        for i in self.text_images:
            self.text_images[i] = GIFImage(
                './sprites/text/{}.gif'.format(self.text_images[i]))
            self.text_images[i].scale(1.0)


class ResultImage(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def update(self, status, screen_size):
        if status == pyBaba.PlayState.WON:
            self.size = max(screen_size[0], screen_size[1]) // 2
            self.image = pygame.transform.scale(pygame.image.load(
                './sprites/won.png'), (self.size, self.size))
            self.rect = self.image.get_rect()
            self.rect.center = (screen_size[0] // 2, screen_size[1] // 2)
        else:
            self.size = max(screen_size[0], screen_size[1]) // 2
            self.image = pygame.transform.scale(pygame.image.load(
                './sprites/lost.png'), (self.size, self.size))
            self.rect = self.image.get_rect()
            self.rect.center = (screen_size[0] // 2, screen_size[1] // 2)

"""Pickle soup server."""

from base64 import b64decode
import binascii
from collections import Counter
import pickle
from pickle import UnpicklingError


BANNER: str = '\n'.join((
    '                                (                ',
    '                             )    )              ',
    ' ._  o  _ |  |  _         _.(--"("""--.._        ',
    ' |_) | (_ |< | (/_       /, _..-----).._,\'      ',
    ' |  _  _      ._        |  `\'\'\'-----\'\'\'`  |',
    '   _> (_) |_| |_)        \\      .-.      /      ',
    '              |           \'.    ._.    .\'      ',
    '                           \'\'--.....--\'\'     ',
))


def get_super_secret_pickle_soup_recipe() -> list[str]:
    """The one and only recipe for the perfect pickle soup."""

    return open('recipe.txt', 'r').read().splitlines()


def make_soup() -> None:
    """Makes a delicious pickle soup using ingredients provided by the user."""

    ingredients: list[str] = []
    while data := input():
        if data == 'done':
            break

        try:
            data = b64decode(data)
        except binascii.Error:
            print('base64 is the only language i understand!')
            return

        if len(data) > 64:
            print('i don\'t remember an ingredient this long...')
            return

        try:
            ingredient = pickle.loads(data)
        except EOFError:
            return
        except UnpicklingError:
            print('invalid pickle!')
            return

        if ingredient in get_super_secret_pickle_soup_recipe():
            print(f'{ingredient!r} is part of the recipe.')
        else:
            print(f'{ingredient!r} is not part of the recipe.')

        ingredients.append(ingredient)

    if not ingredients:
        return

    if Counter(ingredients) == Counter(get_super_secret_pickle_soup_recipe()):
        print('Congratulations! You made an excellent pickle soup!')
    else:
        print('You did not follow the original recipe. Try again.')


def main() -> None:
    """Main function."""

    print(BANNER)
    print()
    print('Send me pickles!')

    make_soup()


if __name__ == '__main__':
    main()

import {GameKey} from "../share/input/game_keys";

export const KEY_MAP: {[key: string]: GameKey} = {
    'w': GameKey.MoveUp,
    'W': GameKey.MoveUp,
    'a': GameKey.MoveLeft,
    'A': GameKey.MoveLeft,
    's': GameKey.MoveDown,
    'S': GameKey.MoveDown,
    'd': GameKey.MoveRight,
    'D': GameKey.MoveRight,
    'e': GameKey.Interact,
    'E': GameKey.Interact,
    'ArrowUp': GameKey.MoveUp,
    'ArrowLeft': GameKey.MoveLeft,
    'ArrowDown': GameKey.MoveDown,
    'ArrowRight': GameKey.MoveRight,
    ' ': GameKey.Interact
};

by Hidden Investigations
Miscellaneous
A tiny terminal arcade game, served over a single TCP connection. You are a dot in a Pac-Man-style maze: collect pellets, dodge the patrolling warden, and explore. Dead in the centre is a vault — walled off with its own distinct tile and sealed on every side. The prize sits inside it.

There is no key, no switch, no hidden door. By the ordinary rules of movement the vault simply cannot be entered, and the movement code holds up to any amount of poking. The way in is not a game mechanic — it is a genuine mistake in the engine itself, and finding it means reverse engineering the provided game binary: understanding how the maze is stored, how the renderer decides what you can see, and the one place where that visibility code reaches into the map with a hand-rolled index. Get a single step of that arithmetic to land where the author never expected, and a wall becomes a floor.

The game binary is in the download; the live service runs that exact binary. The validation token is minted per instance and only appears on a genuine win.

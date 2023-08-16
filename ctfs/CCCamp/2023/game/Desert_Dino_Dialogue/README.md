Welcome to the "Desert Dino Dialogue" challenge, where you will embark on a unique and captivating encounter in the scorching desert. Deep within the arid landscape, hidden behind towering mountains, resides a lonely NPC (Non-Player Character) like no other—a talking dinosaur longing for a conversation.
Your task is to engage in an extended conversation with this fascinating desert-dweller. The dinosaur, with its ancient wisdom and boundless tales, awaits someone who can listen patiently and provide companionship. As the sweltering sun beats down upon the desert, only the most persevering challengers will succeed in breaking through the dinosaur's initial reserve to unearth its treasure trove of knowledge.
The key to this challenge lies in building a rapport with the dinosaur. Though initially wary and hesitant, it will gradually warm up to you as you demonstrate genuine interest and empathy. The NPC's experiences span centuries, ranging from tales of long-lost civilizations to the secrets of survival in the unforgiving desert. Show your dedication, and it will reveal hidden clues that can be utilized in future challenges.
As you converse with the dinosaur, be mindful of the surrounding environment. The desert can be treacherous, with blistering winds, sandstorms, and dangerous wildlife. Maintain your focus and stay resilient, for every conversation carries the potential to unlock new avenues of exploration.
Remember, the objective of this challenge is to establish a meaningful connection with the dinosaur by actively listening and engaging in a dialogue. Patience and perseverance are the keys to success in unraveling the secrets of the desert and earning the respect of this ancient creature.
Are you ready to delve into the heart of the desert, behind the mountains, to converse with the last remaining dinosaur? Prepare yourself for a journey of discovery, where a simple conversation may hold the key to untold mysteries and open doors to unimaginable possibilities.
Good luck, brave challenger! The desert awaits your arrival, and the dinosaur yearns for someone to share its stories with.


# Game

The game runs under Unix and Windows alike. Do not use WSL if you are on a windows system.

## Credentials
The password is always `password123`. This is plenty secure ;)
Your username is your team name with one digit appended e.g. `ALLES!1`.
When testing on a local server you can use the username in the same pattern, but with `User` as the team name.

## Local run instructions (NixOS)

Run `nix develop`
To run the client use `client` in the client directory
> on non nixos-systems run `nixGLIntel client` in the server directory
To run the server use `server --auth_path src/server/server/map/users.json`

use `-v` for more verbose output

## Local run instructions (server)
1. Run the `docker-compose.yml1` inside the db directory to start the clickhouse
2. Install poetry.
3. Use `poetry install` to get the dependencies and venv
4. Use `poetry run server --auth_path src/server/server/map/users.json` to start the server

## Local run instructions (client)
1. Install poetry.
2. Use `poetry install` to get the dependencies and venv
3. Use `poetry run client --host [gamehost] --port [port]` to start the client. If the `host` and `port` parameters are omitted, the localhost is used. Use `--ssl` to enable ssl

## Protobuf
To (re)generate the protobuf, use `betterproto`. To install use the latest beta via `pip install --pre betterproto`

Then use `buf generate` to generate the files.
`cd proto && buf generate`

## Tiled Properties
Do not use the tiled property class editor. Edit the classes and enums inside the `src/server/server/game/map/properties.py` file and execute `map/generate_properties.py` afterwards. 
Now you can use and access the classes inside of tiled and use the from_dict method to access the properties in your code.


## Assets
https://limezu.itch.io/
https://twitter.com/ScissorMarks https://arks.itch.io/dino-characters
https://demching.itch.io/dino-family
Aleksandr Makarov https://iknowkingrabbit.itch.io/heroic-overworld
https://chromium.googlesource.com/

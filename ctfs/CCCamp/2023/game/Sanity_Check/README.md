Talk to Kuro and learn about this wonderful dino land you landed in.
Before you can do that, you have to get the client (and local server) running. Here are some primers to get started:
We use poetry to manage the python venv and all dependencies. Check out the poetry docs how to install poetry
You need python >= 3.10, otherwise the game won't start
Use poetry install in the root directory to do all the magic.
If you use Ubuntu, poetry might being stuck resolving dependencies. Disabling they keyring support might solve this: export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring before poetry install
If you encounter errors regarding *.gif animations when starting the game, make sure to install gdk-pixbuf and gdk-pixbuf-xlib (or use the nix flake)
After installation, check out the README.md to get the server running. The server allows you to better understand the game, but has some limitations:
You only get access to a test map in JSON format
The flags are redacted (duh)
Some modules are missing, like the source code of the native folder
Note: You can't use ncat to connect to the game server directly. Use the game client instead. The ncat command below is just for copy and paste convenience. Read the README.md for further instructions!


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

Even dinos sometimes get lost. Find the lost dino and race to him as fast as possible. Otherwise, it might be to late!


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

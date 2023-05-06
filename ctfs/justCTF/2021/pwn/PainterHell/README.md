When I was very young, I made mods for various games. I think I was developing very secure plugins at the time. Can you check my old plugins?

BTW you don't need to exploit the TF2 game engine!

Hints:

    Sandbox setup info. We are only changing outside ports. All ports inside container are same like in task.zip. Our example sandbox docker-compose looks like:

    ports:
      - 27016:27015/udp
      - 27016:27015/tcp
      - 81:80

    Have you found the backdoor?
    Backdoor is connected somehow with django app.

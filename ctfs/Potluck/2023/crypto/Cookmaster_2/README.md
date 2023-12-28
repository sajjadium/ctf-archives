It's the potluck season again! But as every year, that damn dude Jerry brought his special Cookmaster and is stealing the show with his secret sauce! But not this year. It's time to teach him a lesson! Can you steal the recipe for his secret sauce and corrupt his Cookmaster to put a bad taste to his food?
You even bought your own Cookmaster to try everything before you can pull of your heist during the potluck!
Flag 1: Can you access the system and extract the secret sauce? Flag 2: Great, you got system access! Now all that’s left to do, hack the system and corrupt the heater to grill his sauce!


# cookmaster - Potluck CTF 2023

Starting the interface from the root folder with `docker compose up`
should set everything up out of the box, and open a web interface on
localhost at port 31337. You might have to `modprobe vcan` (e.g. on
Ubuntu this requires you installing extra kernel modules)
and `modprobe vxcan` and some shenanigans for running the
docker-in-docker setup.

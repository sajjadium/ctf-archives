We went down the unlucky path of setting up a mastodon just for you! Just jokes. My Boss gave me a notice on my lacking perfomance, my monthly quota of exploits is too low. Can you help me, pal?

Please develop your exploit locally and then request your instance to retrieve the flag here:


# Mastodon't

Welcome to the Mastodon't challenge. We were quite unlucky at picking
a commit hash at random (3d8bd093b9197659563070d2c763988428063406)
so we are told to be vulnerable to CVE-2023-36460. 
Luckily there are no public exploits. 

Have fun! 

# Login
User: pwn@mastodont.flu.xxx
Pass: hacklu23

# Local Setup
* Add a `/etc/hosts` entry for `mastodon.local` pointing to `127.0.0.1`
* Run the local setup (traefik as proxy) via: `docker compose -f docker-compose.yml -f docker-compose-local.yml up`
* Visit https://mastodon.local

# Tips
In case you are struggling in the very end, be mindful of caching and just 
write your exploit with a minimal amount of requests. Good luck.

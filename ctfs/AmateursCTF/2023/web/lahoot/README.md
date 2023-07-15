smashmaster
Recently Kahoot decided to limit players to 10 if you don't pay a subscription fee. Since I'm broke, I decided to write my own self-hosted version Kahoot-style game. idk why but my friend thinks the code is a bit cursed.


# Lahoot
Self-hosted Kahoot clone intended for running one game at a time. 
## Installing
If you are on a version of node that is not 16 you might need to `--force` node into installing friendly-words or rewrite the friendly name generator. 
## Flavor
Admins can put their own files into `flavor` to allow for custom sfx. 
## Locking
We use Postgres to lock our async code.

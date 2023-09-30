mbund

The tor-only accessible chatting webapp for ogres!


# Ogrechat

The tor-only accessible chatting webapp for ogres!

http://ogresogtmou2q5uoh3ctyd4wfc4n3pghyxvf4zyi5fm3ou6u5mdyshid.onion/

## Running

```
docker build . -t ogrechat
docker run --rm -it -p 3000:3000 -p 8080:8080 ogrechat
```

Then access [http://localhost:3000](http://localhost:3000) in firefox. The Tor part of this challenge is not included in the challenge distribution files.

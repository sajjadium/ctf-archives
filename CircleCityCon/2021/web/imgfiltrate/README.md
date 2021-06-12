
Hint! In this challenge there are two services: the web app and the admin bot.

docker-compose creates an internal network for these two services, and the web app has an internal hostname set to imgfiltrate.hub.

Note that the admin bot's cookie is set for this internal domain, not the external domain at 35.224.135.84. This means that when you submit a URL to the admin bot, you must do something like:
http://imgfiltrate.hub/<stuff>


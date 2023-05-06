# Sentinel - Flag Secure Computing as a Service

## Introduction
Each user can create his own servlet instance to run arbitrary code

Instances are isolated and won't affect each other

The only catch is that you are not allowed to read the flag

## Requirements
Please refrain from opening multiple instances as this will stress our server, you can always reset your instance from the instance manager

Should you decide to stop using your instance, remove it to free allocated resource

If deemed necessary, admin will reset the entire challenge, effectively wiping any progress stored on server. Announcements will be made before resets

## Hints
You are advised to explore the environment a bit before trying to figure out how to exploit the service

There are no intended bugs in instance manager, focus on sentinel.c instead

## Note
If you are sufficiently confident that your exploit should work, and have tested and succeeded locally, feel free to contact admin

Be informed that we are fairly confident the intended solution will work without trouble most of the time

"dummySecret" is just a placeholder of secret key for admin to healthcheck service effeciently, don't waste your time attempting this

Obviously, "BALSN{real flag}" is not the real flag, but if you insist...

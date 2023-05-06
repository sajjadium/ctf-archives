# Lord of the Flag: The Unfinished Chat

Guideline for local setup:

You are given three binaries - one for OSX, Windows and Linux.


First, you need to create a Firebase project at https://firebase.google.com/ and enable the Firestore Database in test mode. After that is done, go to Project Settings and add a new Web App. This will generate a firebase config which you can use to fill out the `.pbchatrc` file and place it in your home directory (make sure the keys are quoted so it's valid json).

Go to the Authentication tab and enable the Email/Password sign-in provider.

(optional) Under Rules section, paste the content of `firestore.rules` if you want to replicate the production rules.

The admin user requires a token to login, which is craeted using a service account key. This can be generate in the firebase console -> Project settings -> Service accounts -> Firebase Admin SDK -> Generate new private key.

Move the downloaded json file to `admin/serviceAccountKey.json` and run `node token.js > admin-token.env` to get the ADMIN_ROOM and ADMIN_TOKEN.

Once that is done, you can run `docker-compose up --build` to start the service.

This will spin up a container and expose VNC on port 15900 which you can access with password "hunter2" and you can verify that "Sauron" has it's chat open. 

Thereafter, use client binary of your choice, to register an account with the exact roomcode you just selected admin token for. 

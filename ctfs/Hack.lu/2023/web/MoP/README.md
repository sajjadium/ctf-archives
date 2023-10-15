Are you afraid of ghosts? It is rumored that some can be seen on my challenge graveyard at https://ctf.localo.ooo.

It is said that you have two choices when encountering one. Will you use your virtual vacuum to vanquish it, or shall you tread cautiously and report the ghost to the admin?

Rumors also abound that the admin, shrouded in secrecy, possesses a cryptic flag, a symbol of their dominion over the graveyard. This elusive treasure, however, lies hidden deep within the bowels of their hard drive, an impenetrable fortress, or so it seems...

This setup uses the KISS challenge broker which sometimes gets stuck, if that is the case just try to reload.

The challenge container itself won't have internet access!

If you have nix installed, you can easily get a dev environment with all dependencies using

    nix develop
    cd app
    mvn package
    java -jar target/app-1.0.jar (use nix --extra-experimental-features "nix-command flakes" develop if you don't have flakes enabled)

(I have also included the Dockerfile that is used on the challenge server)

The setup might look intimidating if you are unfamiliar with nix, you should be able to replicate a similar setup by using these steps on any modern linux distro

    install jdk17
    install maven
    install chromium
    install chromedriver (https://chromedriver.chromium.org/)
    set CHROME_BINARY env var to you chromium binary path, make sure that is in PATH
    switch to app directory and run mvn package
    after that you should be able to start the server using java -jar target/app-1.0.jar

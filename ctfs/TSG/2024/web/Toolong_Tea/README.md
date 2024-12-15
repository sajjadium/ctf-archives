Author: fabon

    Recently it's getting colder in Tokyo which TSG is based in. Would you like to have a cup of hot oolong tea? It will warm up your body.
    Hint for beginners
        First of all, please open the given website and play around with it. This challenge claims that you can get the flag by sending the number 65536 to the server, but it quickly turns out that the story isn't that simple.
        Next, please read the attached source code. The file server.js contains the important logic of this website. The flag is stored in a variable called flag, so the purpose is to leak this value.
        There is a bug which can be exploited to get the flag. Some knowledge of web technologies, especially JavaScript, may be required, so please refer to documentation such as MDN if necessary.
        You can run this website locally as usual Node.js app (npm install && node server.js), or via docker compose (docker compose up --build).
        Note that you do not need a large volume of accesses to solve this problem. Please refrain from mass access similar to DoS.

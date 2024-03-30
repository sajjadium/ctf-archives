Welcome! Today is your first day as a summer intern at E-Corp (aka Evil Corp aka E-Crime Corp). Your summer project will consist of expanding E-Corp's access to computer networks. Inspired by the Mirai botnet, E-Corp has spun up a new division dedicated to gaining access into IOT devices. Your summer project will be to find and exploit a vulnerability in a modern router. A fellow intern has already found a stack pointer leak, so you know that a stack pointer on the server is 0x7c974a30. Good luck!

The hosted website is an emulated version of a real router bought on Amazon. The emulated firmware was dumped directly off a real device. If your exploit is written well, it will work on real routers in the wild. Please use your exploit responsibly - ISSS claims no responsiblity for your behavior. If you find a zero day, please disclose it appropriately to the relevant manufacturer(s). A script will automatically restart the router if it has crashed. If you can't access it after 10 minutes, please message an officer.

The firmware can be found here.

    Note that due to networking constraints, you will need to connect over a bind shell. Ports 1336-1440 inclusive will be forwarded to the router.

By Aadhithya (@aadhi0319 on discord)

const readline = require("readline");
const net = require("net");
const { browse, isValidUrl } = require("./utils");
const PORT = 1337;

var server = net.createServer();

server.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});

server.on("connection", (socket) => {
  setTimeout(() => socket.destroy(), 30 * 1000);
  try {
    const rl = readline.createInterface({
      input: socket,
      output: socket,
    });
    rl.question("Url to visit => ", async (url) => {
      url = url.trim();
      if (isValidUrl(url)) {
        await browse(url);
        socket.write('Done!');
      }
      rl.close();
      socket.destroy();
    });
  } catch {
    socket.write("Oops, something went wrong");
  }
});

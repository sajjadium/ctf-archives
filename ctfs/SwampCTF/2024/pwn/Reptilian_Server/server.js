const vm = require('node:vm');
const net = require('net');

// Get the port from the environment variable (default to 3000)
const PORT = process.env.PORT || 3000;

// Create a TCP server
const server = net.createServer((sock) => {
    console.log('Client connected!');
    sock.write(`Welcome to the ReptilianRealm! Please wait while we setup the virtual environment.\n`);

    const box = vm.createContext(Object.create({
        console: {
            log: (output) => {
                sock.write(output + '\n');
            }
        },
        eval: (x) => eval(x)
    }));

    sock.write(`Environment created, have fun playing with the environment!\n`);

    sock.on('data', (data) => {
        const c = data.toString().trim();

        if (c.indexOf(' ') >= 0 || c.length > 60) {
            sock.write("Intruder Alert! Removing unwelcomed spy from centeralized computing center!");
            sock.end();
            return;
        }

        try {
            const s = new vm.Script(c);
            s.runInContext(box, s);
        } catch (e) {
            sock.write(`Error executing command: ${e.message} \n`);
        }
    });

    sock.on('end', () => { console.log('Client disconnected!'); });
});

// Handle server errors
server.on('error', (e) => {
    console.error('Server error:', e);
});

// Start the server listening on correct port.
server.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});

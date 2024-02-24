const {visit}= require('./bot')

const net = require('net');

const port = 8080; 

const server = net.createServer();

server.on('listening', () => {
    console.log(`Server listening on port ${port}`);
});

server.on('connection', (socket) => {
    console.log('Client connected');
    socket.write('Enter url :')

   
    socket.on('data', async(data) => {
        
        console.log(data.toString('utf8'))
       
        await visit(data.toString('utf8'))
        socket.write('bot visited');
    });

   
    socket.on('close', () => {
        console.log('Client disconnected');
    });
});

server.listen(port, () => {
    console.log(`Server started on port ${port}`);
});

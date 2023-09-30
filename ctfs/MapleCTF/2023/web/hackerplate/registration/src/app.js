import server from './server.js';

const PORT = process.env.INTERNAL_PORT || 8081;

server.listen(PORT, () => {
    console.log(`registration listening on port ${PORT}`);
})

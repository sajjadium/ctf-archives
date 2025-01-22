import express from 'express';

const app = express();
const port = 3000;

app.get('/', (req, res) => {
    res.send('Hello from TypeScript Node.js Server!');
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:\${port}/`);
});

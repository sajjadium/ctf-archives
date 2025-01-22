const express = require('express');
const app = express();
const bodyParser = require('body-parser');

let todos = [];

app.use(bodyParser.json());

app.get('/todos', (req, res) => {
    res.json(todos);
});

app.post('/todos', (req, res) => {
    const todo = { id: Date.now(), task: req.body.task };
    todos.push(todo);
    res.json(todo);
});

app.delete('/todos/:id', (req, res) => {
    todos = todos.filter(todo => todo.id != req.params.id);
    res.json({ success: true });
});

app.listen(3000, () => {
    console.log('To-Do app listening on port 3000');
});

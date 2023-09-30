import express from 'express';
const app = express();
import routes from './routes/index.js';
import mongoose from 'mongoose';
import Cookies from 'cookies';
import morgan from 'morgan';

mongoose.connect('mongodb://localhost:27017/area51', { useNewUrlParser: true , useUnifiedTopology: true });

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(morgan('combined'))

app.use(express.static('static'));
app.set('view engine', 'ejs');

app.use(Cookies.express());

app.use(routes);

app.all('*', (req, res) => {
    return res.status(404).send({
        message: '404 no aliens here'
    });
});

app.listen(80, () => console.log('Listening on port 80'));
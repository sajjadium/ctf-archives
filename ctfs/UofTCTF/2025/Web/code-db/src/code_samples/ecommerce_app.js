const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

// Connect to MongoDB
mongoose.connect('mongodb://localhost/ecommerce', { useNewUrlParser: true, useUnifiedTopology: true });

// Define a Product schema
const productSchema = new mongoose.Schema({
    name: String,
    price: Number,
    inStock: Boolean
});

const Product = mongoose.model('Product', productSchema);

// Routes
app.get('/products', async (req, res) => {
    const products = await Product.find();
    res.json(products);
});

app.post('/products', async (req, res) => {
    const newProduct = new Product(req.body);
    await newProduct.save();
    res.json(newProduct);
});

app.put('/products/:id', async (req, res) => {
    const updatedProduct = await Product.findByIdAndUpdate(req.params.id, req.body, { new: true });
    res.json(updatedProduct);
});

app.delete('/products/:id', async (req, res) => {
    await Product.findByIdAndDelete(req.params.id);
    res.json({ message: 'Product deleted' });
});

app.listen(3000, () => {
    console.log('E-commerce app listening on port 3000');
});

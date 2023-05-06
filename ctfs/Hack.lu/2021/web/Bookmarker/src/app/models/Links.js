const mongoose = require('mongoose')

const Linksschema = new mongoose.Schema({
    username: {
        type: String,
        required: true
    },
    title: {
        type: String,
        required: true
    },
    url: {
        type: String,
        required: true
    },
    hash: {
        type: String,
        required: true
    },
    date: {
        type: String,
        default: Date.now()
    }

})

const Links = mongoose.model('Links', Linksschema)
module.exports = Links



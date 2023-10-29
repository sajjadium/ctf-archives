const mongoose = require('mongoose');

var schema = new mongoose.Schema({
    Username : {
        type : String,
        unqiue: true,   
        required: true
    },
    Password: {
        type : String,
        required: true
    }
})

const UserCol = mongoose.model('users', schema);
 
module.exports = UserCol;
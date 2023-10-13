const mongoose = require('mongoose')

const UserSchema = new mongoose.Schema({
    username: {
        type: String,
        required: true
    },
    password: {
        type: String,
        required: true
    },
    date: {
        type: String,
        default: Date.now()
    }
})

const User = mongoose.model('User', UserSchema)


// add Admin
User.findOneAndUpdate({
    username: process.env.ADMIN_USERNAME,
}, {
    password: process.env.ADMIN_PASSWORD
}, {
    upsert: true,
    new: true
})
.then(console.log('[+] Admin added'))
.catch(err => console.log(err))


module.exports = User



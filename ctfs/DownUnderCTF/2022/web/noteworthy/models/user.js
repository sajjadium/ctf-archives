const mongoose = require('mongoose')
const passportLocalMongoose = require('passport-local-mongoose')

const userSchema = new mongoose.Schema({
    username: {
        type: String,
        required: true
    },
    password: {
        type: String
    },
    notes: {
        type: [{
            type: mongoose.Schema.Types.ObjectId,
            ref: 'Note'
        }]
    }
})

userSchema.plugin(passportLocalMongoose, {
    session: false
})

module.exports = mongoose.model('User', userSchema)

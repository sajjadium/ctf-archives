const mongoose = require('mongoose')
const crypto = require('crypto')

const PadSchema = new mongoose.Schema({
    uniqueId: {
        type: String,
        required: true,
        default: () => crypto.randomBytes(24).toString('hex'),
        index: { unique: true },
    },
    title : {
        type: String,
        required: true,
        default: "Untitled"
    },
    username: {
        type: String,
        required: true,
        index: true 
    },
    content: {
        type: String,
        required: true,
        default: "Your content here :)"
    },
    createdAt: {
        type: Date,
        expires: 3*60,
    },
    isPublic: {
        type: Boolean,
        default: false
    }
})

const Pad = mongoose.model('Pad', PadSchema)

module.exports = Pad



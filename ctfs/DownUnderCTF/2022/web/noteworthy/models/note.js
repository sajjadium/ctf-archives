const mongoose = require('mongoose')

const noteSchema = new mongoose.Schema({
    owner: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    noteId: {
        type: Number,
        required: true,
        index: true,
        unique: true
    },
    contents: {
        type: String,
        required: true,
        default: ''
    }
})

module.exports = mongoose.model('Note', noteSchema)

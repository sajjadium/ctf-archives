const fs = require('fs')
const session = require('express-session')

const noop = () => { }
const DEFAULT_OPTS = {
    dir: './sessions'
}

class FSStore extends session.Store {
    constructor(options = DEFAULT_OPTS) {
        super(options)
        this.options = options
    }

    get(sid, cb = noop) {
        fs.readFile(`${this.options.dir}/${sid}/session.json`, 'utf8', (err, d) => {
            if (err) return cb(err)
            if (!d) return cb()
            return cb(null, JSON.parse(d))
        })
    }

    set(sid, sess, cb = noop) {
        fs.mkdir(`${this.options.dir}/${sid}`, { recursive: true }, (err) => {
            if (err) return cb(err)
            fs.writeFile(`${this.options.dir}/${sid}/session.json`, JSON.stringify(sess), (err) => {
                return cb(err)
            })
        })
    }

    destroy(sid, cb = noop) {
        fs.rmdir(`${this.options.dir}/${sid}`, { recursive: true }, (err) => {
            return cb(err)
        })
    }
}

module.exports = FSStore


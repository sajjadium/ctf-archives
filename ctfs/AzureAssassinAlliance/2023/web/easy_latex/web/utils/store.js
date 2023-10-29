const crypto = require('crypto');

class Store {
    constructor(){
        this.store = new Map()
    }
    get(id){
        return this.store.get(id)
    }
    add(obj){
        const id = crypto.randomBytes(3).toString('hex')
        this.store.set(id, obj)
        return id
    }
}

module.exports.Store = Store
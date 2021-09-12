const crypto = require('crypto')
const mongodb = require('mongodb')

const mongoUrl = 'mongodb://db:27017'

const connect = async () => {
    return await mongodb.MongoClient.connect(mongoUrl)
}


const init = async client => {


    let users = client.db('test').collection('users')
    users.deleteMany(err => {
        if (err) {
            console.log(err)
        } else {
            users.insertOne({
                username: 'rabbit',
                password: crypto.randomBytes(32).toString('hex'),
                active: true
            })
        }
    })

    let images = client.db('test').collection('candies')
    images.deleteMany(err => {
        if (err) {
            console.log(err)
        } else {
            images.insertMany(
                [
                    {
                        id: '1',
                        file: '1.png',
                        name: 'bunny_candy',
                        description: 'So sweet!!!'
                    }
                ]
            )
        }
    })

}

class Users {

    static add = async (username, password, active) => {
        let user = {
            username: username,
            password: password,
            active: active
        }
        let client = await connect()
        await client.db('test').collection('users').insertOne(user)
    }


    static find = async query => {

        let client = await connect()
        let rec = await client.db('test').collection('users').findOne(query)
        return rec
    }


}

class Candies {

    static list = async () => {
        let candies = []
        let client = await connect()
        await client.db('test').collection('candies').find().forEach(candy => candies.push(candy))
        return candies
    }

    static find = async query => {
        let client = await connect()
        let rec = await client.db('test').collection('candies').findOne(query)
        return rec
    }

}

connect()
    .then(init)
    .catch(console.log)

module.exports = {
    Users,
    Candies
}
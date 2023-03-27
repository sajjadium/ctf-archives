import { GraphQLError } from 'graphql';
import jwt from 'jsonwebtoken'

const register = async (_parent, {username, password}, context) => {
    console.log('authResolvers: register(' + username + ':' + password + ')')

    try{
        await context.dataSources.db.register(username, password)
    } catch (err) {
        console.error(err)
        throw new GraphQLError('registration failed')
    }

    return true
}

const login = async (_parent, {username, password}, context) => {
    console.log(`authResolvers: login(${username}:${password})`)
    
    try {
        const user = await context.dataSources.db.getUserByUsername(username, password)
        if (user.password === password) {
            return jwt.sign({sub: user.id, isAdmin: user.isadmin}, process.env.SECRET_KEY || 'secretkey')
        } else {
            throw new GraphQLError('login failed')
        }
    } catch (err) {
        console.error(err)
        throw new GraphQLError('login failed')
    }
}

export default {
    register,
    login
}
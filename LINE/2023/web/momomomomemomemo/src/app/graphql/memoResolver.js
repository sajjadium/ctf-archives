import { GraphQLError } from 'graphql';
import jwt from 'jsonwebtoken'

const addMemo = async (_parent, {token, content}, context) => {
    const decoded = verifyJWT(token)

    console.log(`memoResolver: addMemo(${decoded.sub},${content})`)

    try{
        await context.dataSources.db.addMemo(decoded.sub, content)
    } catch (err) {
        console.error(err)
        throw new GraphQLError('addMemo failed')
    }

    return true
}

const memos = async (_parent, {token}, context) => {
    const decoded = verifyJWT(token)

    console.log(`memoResolvers: memos(${decoded.sub})`)

    let ownedMemos;
    try {
        ownedMemos = await context.dataSources.db.getOwnedMemos(decoded.sub)
    } catch (err) {
        console.error(err)
        throw new GraphQLError('memos failed')
    }
    return ownedMemos
}

const memo = async (_parent, {token, id}, context) => {
    const decoded = verifyJWT(token)

    console.log(`memo (${decoded.sub}, ${id})`)

    let viewableMemo;
    try {
        if (decoded.isAdmin) {
            viewableMemo = await context.dataSources.db.getMemo(id)
        } else {
            viewableMemo = await context.dataSources.db.getOwnedMemo(decoded.sub, id)
        }
    } catch (err) {
        console.error(err)
        throw new GraphQLError('memo failed')
    }
    return viewableMemo
}

const verifyJWT = (token) => {
    try {
        const decoded = jwt.verify(token, process.env.SECRET_KEY || 'secretkey')
        return decoded
    } catch(err) {
        throw new GraphQLError('invalid token', {
            extensions: {
                code: 'UNAUTHORIZED'
            }
        })
    }
}

export default {
    addMemo,
    memos,
    memo
}
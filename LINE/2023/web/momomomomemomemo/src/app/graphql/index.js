import { ApolloServer } from '@apollo/server'
import authResolvers from './authResolvers.js'
import bugReportResolver from './bugReportResolver.js'
import memoResolver from './memoResolver.js'

const resolvers = {
    Mutation: {
        register: authResolvers.register,
        login: authResolvers.login,
        addMemo: memoResolver.addMemo,
        reportBug: bugReportResolver.reportBug,
        getCaptchaImage: bugReportResolver.getCaptchaImage
    },
    Query: {
        memos: memoResolver.memos,
        memo: memoResolver.memo
    }
}

const typeDefs = `#graphql
    type Memo {
        id: String!
        ownerId: String!,
        content: String!
    }

    type Mutation {
        register (
            username: String!,
            password: String!
        ): Boolean

        login (
            username: String!,
            password: String!
        ): String

        addMemo (
            token: String!,
            content: String!
        ): Boolean

        reportBug (
            token: String!,
            url: String!,
            captchaCode: String!
        ): Boolean

        getCaptchaImage (
            token: String!
        ): String
    }

    type Query {
        memos (
            token: String!
        ): [Memo]

        memo (
            token: String!
            id: String!
        ): Memo
    }
`


const apolloServer = new ApolloServer({
    typeDefs,
    resolvers,
    includeStacktraceInErrorResponses: false,
    formatError: (formattedErr, origError) => {
        delete formattedErr.locations
        delete formattedErr.path
        return formattedErr
    }
})

export { apolloServer }
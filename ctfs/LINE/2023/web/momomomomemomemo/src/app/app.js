import { expressMiddleware } from '@apollo/server/express4';
import pkg from 'body-parser';
const { json } = pkg;
import express from 'express';
import http from 'http';
import db from './db/index.js'
import Redis from 'ioredis'
import crypto from 'crypto'

import { apolloServer } from './graphql/index.js'

process.env.SECRET_KEY = crypto.randomBytes(32).toString('base64')

import dotenv from 'dotenv'
dotenv.config()

var app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

await apolloServer.start()


const redis = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: 6379,
  password: process.env.REDIS_PASSWORD || ''
})
redis.on('error', err => {
  console.error('Redis error: ' + err)
})

await redis.set('reported_count', 0)
await redis.set('proceeded_report_count', 0)

app.use('/graphql', json(), expressMiddleware(apolloServer,{
    context: async () => {
        return {
            dataSources: {
                db,
                redis
            }
        }
    }
}));

// simple i18n
app.use(function (req, res, next) {
    let origPath = req.originalUrl.split('?')[0]
    let origParam = req.originalUrl.split('?')[1]
    let langPath = 'en/'
    
  
    if (origPath.match(/((\/en\/?)|(\/ja\/?))$/) || origPath.match(/^(\/static\/|\/graphql\/?|\/favicon.ico\/?)/)) {
      next()
    } else {
      if (req.headers['accept-language'] && req.headers['accept-language'].split(',')[0] === 'ja') langPath = 'ja/'
      res.redirect(origPath + (origPath.endsWith('/') ? '' : '/') + langPath + (origParam ? '?' + origParam : ''))
    }
  })
  
app.use('/', express.static('public'))

const httpServer = http.createServer(app);
await new Promise((resolve) => httpServer.listen({ port: 4000 }, resolve));

const { connectDB, initApp } = require('./server/app')

const PORT = process.env.PORT || 3000
const dbName = 'noteworthy'
const DB_URI = process.env.MONGO_CONNECTION_URI || `mongodb://127.0.0.1:27017/${dbName}`

connectDB(DB_URI, dbName).then(async () => {
    const app = await initApp()
    app.listen(PORT, () => {
        console.log(`Server listening on port ${PORT}`)
    })
})

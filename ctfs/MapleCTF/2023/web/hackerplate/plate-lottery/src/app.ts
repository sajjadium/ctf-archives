import { server } from "./server.js"
import { PORT } from "./util/constants.js"

server.listen(PORT, () => {
    console.log(`plate lottery portal listening on port ${PORT}`)
})
import { authCheck, checkToken } from './auth'
import { CONFIG } from './config'


const auth = (req, res)=>{
    let _username = req.headers[CONFIG.header.username]
    let _password = req.headers[CONFIG.header.password]
    res.end(JSON.stringify(authCheck(_username, _password)))
}

const getFlag = (req, res)=>{
    let token = req.headers['x-token']
    if(checkToken(token)) {
        res.end(JSON.stringify({'result': true, 'flag': CONFIG.flag }))
    } else {
        res.end(JSON.stringify({'result': false}))
    }
}

export function router (req, res, path) {
    switch(path){
        case '/auth':
            auth(req, res)
            break;
        case '/flag':
            console.log("Access /flag endpoint. ")
            getFlag(req, res)
            break;
        default:
            res.end(JSON.stringify({"result": false}))
            break;
    }
}
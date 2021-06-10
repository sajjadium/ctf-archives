import jwt from 'jsonwebtoken';
import { CONFIG } from './config'


const encode = (data)=>jwt.sign(data, CONFIG.secret, { algorithm: 'HS256'})

const verify = (token)=>jwt.verify(token, CONFIG.secret, { algorithm: 'HS256'}, (err)=>{if(err){return false;} return true;})

const decode = (token)=>jwt.decode(token)

const authCheck = (username, password)=>{
    let result = false;
    let token = ''
    if(username === CONFIG.admin.username && password === CONFIG.admin.password){
        result = true
        token = encode({user: username, role: 'admin'})
    }
    return {result, token}
}

const checkToken = (token)=>{
    if(verify(token)) {
        if(decode(token)["role"] === 'admin') return true
        return false
    }
    return false
}

export {authCheck, checkToken}
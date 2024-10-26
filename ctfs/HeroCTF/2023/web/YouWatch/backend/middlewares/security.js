const jwt = require('jsonwebtoken');
const userModel = require('../models/userModel');

exports.checkJWT = async (req, res, next) => {
    let token = req.cookies['token'];
    if(token)
    {
        jwt.verify(token, process.env.SECRET_KEY, (err, decoded) => {
            if(err)
            {
                return res.status(401).json({"code":401,"error":"Invalid token"})
            }
            else
            {
                req.decoded = decoded
                const expiresIn = 24 * 60 * 60;
                const newToken  = jwt.sign({
                    id: decoded.id,
                    pseudo : decoded.pseudo,
                    email: decoded.email
                },
                process.env.SECRET_KEY,
                {
                    expiresIn: expiresIn
                });
                res.cookie('token',newToken,{httpOnly: true, maxAge: 1000 * 60 * 60, SameSite: "lax"})
                next();
            }
        })
    }
    else
    {
        return res.status(401).json({"code":401,"error":"Token required"})
    }
}

exports.isLogged = async (req,res,next) => {
    let token = req.cookies['token'];
    if(token)
    {
        jwt.verify(token, process.env.SECRET_KEY, (err, decoded) => {
            if(err)
            {
                next();
            }
            else
            {
                return res.status(400).json({"code":400,"error":"User is already logged in"});
            }
        })
    }
    else
    {
        next();
    }
}

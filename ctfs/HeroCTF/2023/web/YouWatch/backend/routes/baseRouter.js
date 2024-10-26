const express = require("express");
const router = express.Router();
const {sequelize, User} = require("../models/")
const sha256 = require('sha256');
const {checkType} = require("../functions")
const security = require("../middlewares/security")
const jwt = require('jsonwebtoken');

router.post("/login", security.isLogged, async(req,res) => {
    if(req.body.pseudo != undefined && req.body.password != undefined)
    {
        if(checkType(req.body.pseudo) && checkType(req.body.password))
        {
            let pseudo = req.body.pseudo
            try
            {
                const user = await User.findOne({
                    where: {pseudo}
                })
                if(user)
                {
                    if(user.password === sha256(req.body.password))
                    {
                        const expireIn = 24 * 60 * 60;
                        const token    = jwt.sign({
                            id: user.id,
                            pseudo: pseudo,
                            email: user.email
                        },
                        process.env.SECRET_KEY,
                        {
                            expiresIn: expireIn
                        });
                        res.cookie('token',token,{httpOnly: true, maxAge: 1000 * 60 * 60, SameSite: "lax"})
                        res.status(200).json({"code":200,"ok":"User connected"})
                    }
                    else
                    {
                        res.status(403).json({"code":403,"error":"Invalid credentials"})
                    }
                }
                else
                {
                    res.status(403).json({"code":403,"error":"Invalid credentials"})
                }
            }catch(err)
            {
                res.status(500).json({"code":500,"error":"Internal server error"})
            }
        }
        else
        {
            res.status(400).json({"code":400,"error":"At least one parameter is not a string"})
        }
    }
    else
    {
        res.status(400).json({"code":400,"error":"Missing parameters"})
    }
})

router.post("/register", security.isLogged, async(req,res) => {
    if(req.body.pseudo != undefined && req.body.email != undefined && req.body.password != undefined)
    {
        if(checkType(req.body.pseudo) && checkType(req.body.email) && checkType(req.body.password))
        {
            if(req.body.pseudo.length < 20)
            {
                if(req.body.email.length < 60)
                {
                    let pseudo = req.body.pseudo;
                    let email = req.body.email;
                    let password = sha256(req.body.password);
                    try
                    {
			pseudo = pseudo.replaceAll(">","");
			pseudo = pseudo.replaceAll("<","");
                        const user = await User.create({pseudo, email, password})
                        if(user)
                        {
                            res.status(200).json({"code":200,"ok":"User registered"})
                        }
                        else
                        {
                            res.status(500).json({"code":500,"error":"An unknwon error occured, please try again"})
                        }
                    }catch(err)
                    {
                        res.status(400).json({"code":400,"error":"Email must be valid"})
                    }
                }
                else
                {
                    res.status(400).json({"code":400,"error":"Email must be at least 60 caracters"})
                }
            }
            else
            {
                res.status(400).json({"code":400,"error":"Pseudo must be at least 20 caracters"})
            }
        }
        else
        {
            res.status(400).json({"code":400,"error":"At least one parameter is not a string"})
        }
    }
    else
    {
        res.status(400).json({"code":400,"error":"Missing parameters"})
    }
})

router.get("/logout", async(req,res) => {
    res.cookie('token','',{httpOnly: true, maxAge: 0, sameSite: "lax"})
    res.status(200).json({"code":200,"ok":"User logout"})
})

router.get("/profile",security.checkJWT, async(req,res) => {
    console.log(req.decoded)
    res.status(200).json(
        {
            "pseudo": req.decoded.pseudo,
            "email": req.decoded.email
        }
    );
    res.end();
})

module.exports = router

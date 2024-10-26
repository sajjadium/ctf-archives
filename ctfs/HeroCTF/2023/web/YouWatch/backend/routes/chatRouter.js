const express = require("express");
const router = express.Router();
const {sequelize, Message,User,Video} = require("../models/")
const {checkType} = require("../functions")
const security = require("../middlewares/security")
const {v4} = require("uuid")

router.get("/getChat", security.checkJWT, async(req,res) => {
    if(req.query.chatId != undefined)
    {
        if(checkType(req.query.chatId))
        {
            let isPublic = await Video.findAll({
                where:{
                    chatId: req.query.chatId
                },
                attributes: ["isPrivate"]
            })
            if(isPublic)
            {
                let messages = await Message.findAll({
                    where: {chatId: req.query.chatId},
                    attributes: ["content"],
                    include:[{
                        model: User,
                        attributes: ["pseudo"],
                        as: 'users'
                    }],
                })
                res.status(200).json({"code":200,"data":messages})
            }
            else
            {
                let isOwnByUser = await Video.findAll({
                    where:{
                        chatId: req.query.chatId,
                        userId: req.decoded.id
                    }
                });
                if(isOwnByUser.length > 0)
                {
                    let messages = await Message.findAll({
                        where: {chatId: req.query.chatId},
                        attributes: ["content"],
                        include:[{
                            model: User,
                            attributes: ["pseudo"],
                            as: 'users'
                        }],
                    })
                    res.status(200).json({"code":200,"data":messages})
                }
                else
                {
                    res.status(403).json({"code":403,"data":"This video is private."})
                }
            }
        }
        else
        {
            res.status(400).json({"code":400,"error":"At least one parameter is not a string"})
        }
    }
    else
    {
        res.status(400).json({"code":400,"error":"Missing parameter"})
    }
})

router.post("/sendMessage", security.checkJWT, async(req,res) => {
    if(req.body.content != undefined && req.body.chatId != undefined)
    {
        if(checkType(req.body.content) && checkType(req.body.chatId))
        {
            await Message.create({
                id: v4(), userId: req.decoded.id, content: req.body.content, chatId: req.body.chatId
            })
            res.status(200).json({"code":200,"ok":"Message sent !"})
        }
        else
        {
            res.status(400).json({"code":400,"error":"At least one parameter is not a string"})
        }
    }
    else
    {
        res.status(400).json({"code":400,"error":"Missing parameter"})
    }
})

module.exports = router;
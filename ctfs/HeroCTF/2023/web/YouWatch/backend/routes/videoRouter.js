const express = require("express");
const router = express.Router();
const {sequelize, Video,User,Chat} = require("../models/")
const {checkType} = require("../functions")
const security = require("../middlewares/security")
const crypto = require("crypto");
const path = require("path")
const fs = require("fs")
const {v4} = require("uuid");
const jwt = require('jsonwebtoken');
const { Op } = require("sequelize");
require('express-ws')(router);

router.get("/getVideos", security.checkJWT, async(req,res) => {
    try
    {
        let sort_by = "name";
        let order = "ASC";
        let type = "public";
        let name = "";

        if(req.query.sortBy != undefined)
        {
            if(checkType(req.query.sortBy))
            {
                sort_by = req.query.sortBy;
            }
            else
            {
                res.status(400).json({"code":400,"error":"sortBy is not a string"});
                res.end();
            }
        }

        if(req.query.orderBy != undefined)
        {
            if(checkType(req.query.orderBy) && ["ASC","DESC"].includes(req.query.orderBy))
            {
                order = req.query.orderBy
            }
            else
            {
                res.status(400).json({"code":400,"error":"orderBy is not a string or has an invalid value"});
                res.end();
            }
        }

        if(req.query.type != undefined)
        {
            if(checkType(req.query.type) && ["public","private"].includes(req.query.type))
            {
                type = req.query.type
            }
        }

        if(req.query.name != undefined)
        {
            if(checkType(req.query.name))
            {
                name = req.query.name
            }
        }

        let videos = [];
        if(type == "public")
        {
            videos = await Video.findAll({
                include:[{
                    model: User,
                    attributes: ["pseudo"],
                    as: 'users'
                }],
                attributes: ["id","name","chatId"],
                order: [
                    [sort_by, order] 
                ],
                where:{
                    isPrivate: 0,
                    name: {
                        [Op.like]: `%${name}%`
                    }
                }
            });
        }
        else
        {
            videos = await Video.findAll({
                include:[{
                    model: User,
                    attributes: ["pseudo"],
                    as: 'users'
                }],
                attributes: ["name"],
                order: [
                    [sort_by, order] 
                ],
                where:{
                    isPrivate: 1,
                    name: {
                        [Op.like]: `%${name}%`
                    }
                }
            });
        }
        if(videos.length > 0)
        {
            res.status(200).json({"code":200,"data":videos})
        }
        else
        {
            res.status(200).json({"code":200,"data":"No videos found"})
        }
    }catch(err)
    {
        res.status(500).json({"code":500,"data":"Internal server error"})
    }
})

router.get("/myVideos", security.checkJWT, async(req,res) => {
    const videos = await Video.findAll({
        where: {
            userId: req.decoded.id
        },
        attributes: ["id","name","chatId","isPrivate"]
    });
    if(videos)
    {
        res.status(200).json({"code":200,"data":videos})
    }
    else
    {
        res.status(200).json({"code":200, "data":"No videos found"})
    }
})

router.post("/uploadVideo", security.checkJWT, async(req,res) => {
    if(req.body.name != undefined && req.body.isPrivate != undefined && req.body.video)
    {
        if(checkType(req.body.name) && typeof req.body.isPrivate === "number" && checkType(req.body.video))
        {
            if(req.body.name.length < 100)
            {
                if([0,1].includes(req.body.isPrivate))
                {
                    let rand = crypto.randomBytes(20).toString('hex');
                    let pathVideo = `video_${rand}.mp4`;
                    let video_content = new Buffer(req.body.video, 'base64')
                    fs.writeFileSync(`${process.env.VIDEO_PATH}/${pathVideo}`, video_content);
                    let videoId = v4();
                    let chatId = v4();
                    let userId = req.decoded.id;
                    let isPrivate = req.body.isPrivate;
                    let name = req.body.name;
                    const nbMessages = 0;
                    try
                    {
                        const chat = Chat.create({
                            publicId: chatId, nbMessages
                        });
                        if(chat)
                        {
                            const video = Video.create({
                                id: videoId, name, userId, chatId, isPrivate, pathVideo
                            })
                            if(video)
                            {
                                return res.status(200).json({"code":200,"ok":"Video uploaded !"})
                            }
                            else
                            {
                                return res.status(500).json({"code":500,"error":"Impossible to upload video, please try again."});
                            }
                        }
                        else
                        {
                            return res.status(500).json({"code":500,"error":"Impossible to upload video, please try again."});
                        }   
                    }catch(err){
                        return res.status(500).json({"code":500,"error":"Internal server error"})
                    }
                }else
                {
                    res.status(400).json({"code":400,"error":"isPrivate must be 0 or 1"})
                }
            }
            else
            {
                res.status(400).json({"code":400,"error":"Name must be at least 100 caracters"})
            }
        }
        else
        {
            res.status(400).json({"code":400,"error":"One of the parameter has a wrong type"})
        }
    }
    else
    {
        res.status(400).json({"code":400,"error":"Missing parameters"})
    }
})

router.put("/updateVideo", security.checkJWT, async(req,res) => {
    if(req.body.id != undefined && req.body.name != undefined && req.body.isPrivate != undefined)
    {
        if(checkType(req.body.id) && checkType(req.body.name) && typeof req.body.isPrivate === "number")
        {
            if([0,1].includes(req.body.isPrivate))
            {
                let user_videos = await Video.findAll({
                    where: {
                        userId: req.decoded.id,
                        id: req.body.id
                    }
                })
                if(user_videos.length > 0)
                {
                    if(req.body.pathVideo != undefined)
                    {
                        res.status(403).json({"code":403,"error":"You can't update the path to your video."})
                    }
                    else
                    {
                        const res_update = await Video.update(req.body,
                        {
                            where: {id: req.body.id}
                        })
                        if(res_update)
                        {
                            res.status(200).json({"code":200,"ok":"Video modified"})
                        }
                        else
                        {
                            res.status(500).json({"code":500,"error":"Internal server error"})
                        }
                    }
                }
                else
                {
                    res.status(403).json({"code":403,"error":"You didnt own this video"})
                }
            }
            else
            {
                res.status(400).json({"code":400,"error":"isPrivate must be 0 or 1"})
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

router.post("/deleteVideo", security.checkJWT, async(req,res) => {
    if(req.body.id != undefined)
    {
        if(checkType(req.body.id))
        {
            let user_videos = await Video.findAll({
                where: {
                    userId: req.decoded.id,
                    id: req.body.id
                }
            })
            if(user_videos.length > 0)
            {
                await Video.destroy({
                    where: {
                        id: req.body.id
                    }
                })
                res.status(200).json({"code":200,"ok":"Video deleted"})
            }
            else
            {
                res.status(403).json({"code":403,"error":"You dont own this video"})
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
});

router.get("/getVideoInfos", security.checkJWT, async(req,res) => {
    if(req.query.id != undefined)
    {
        try
        {
            if(checkType(req.query.id))
            {
                let video = await Video.findAll({
                    include:[{
                        model: User,
                        attributes: ["pseudo"],
                        as: 'users'
                    }],
                    where:{
                        id: req.query.id
                    },
                    attributes:  ["name","chatId","isPrivate"]
                })
                if(video.length > 0)
                { 
                    res.status(200).json({"code":200,"data":video[0]});
                }
                else
                {
                    res.status(200).json({"code":200,"data":{}});
                }
                
            }
        }catch(err)
        {
            res.status(500).json({"code":500,"error":"Internal Server Error"})
        }
    }
})

router.get("/loadVideo", security.checkJWT, async(req,res) => {
    if(req.query.id != undefined)
    {
        if(checkType(req.query.id))
        {
            try{
                const video = await Video.findAll({
                    where:{
                        id: req.query.id
                    },
                    attributes: ["pathVideo","isPrivate","userId"]
                })
                if(video.length > 0)
                {
                    if(video[0].isPrivate && req.decoded.id !== video[0].userId)
                    {
                        res.status(403).send({"code":403,"error":"You can't watch a private video that don't belong to you."})
                        res.end();
                    }
                    else
                    {
                        const video_content = fs.readFileSync(`${process.env.VIDEO_PATH}/${video[0].pathVideo}`, {encoding: 'base64'})
                        if(video_content)
                        {
                            res.status(200).send({"code":200,"data":video_content})
                            res.end();
                        }
                        else
                        {
                            res.status(500).send({"code":500,"error":"Internal Server Error"})
                            res.end();
                        }
                    }
                }
                else
                {
                    res.status(400).send({"code":400,"error":"Video not found"})
                    res.end()
                }
            }catch(err)
            {
                res.status(500).send({"code":500,"error":"Internal Server Error"})
                res.end();
            }
        }else
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

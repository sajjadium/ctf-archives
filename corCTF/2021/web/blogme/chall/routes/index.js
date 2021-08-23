const express = require("express");
const router = express.Router();

const { User, Post } = require("../src/db.js");
const { requiresLogin } = require("../src/util.js");

router.get("/", async (req, res) => {
    let admin = await User.findByPk("admin");
    res.render("index", { posts: await admin.getPosts() });
});

router.get("/posts", requiresLogin, async (req, res) => {
    let posts = await req.user.getPosts();
    res.render("posts", { posts });
});

router.get("/post/:id", async (req, res) => {
    let id = req.params.id;
    if(!id) {
        return res.redirect("/?error=" + encodeURIComponent("Missing post id"));
    }
    let post = await Post.findByPk(id);
    if(!post) {
        return res.redirect("/?error=" + encodeURIComponent("No post was found with that id"));
    }

    let author = await post.getUser();
    let comments = [];
    for(let c of await post.getComments()) {
        comments.push({ text: c.text, user: await c.getUser() });     
    }
    res.render("post", { post, author, comments });
});

router.get("/profile", requiresLogin, async (req, res) => {
    let files = [];
    if(req.user.user !== "admin") 
        files = await req.user.getFiles();
    res.render("profile", { user: req.user.toJSON(), files });
});

module.exports = router;
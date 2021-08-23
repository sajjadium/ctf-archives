const fetch = require("node-fetch");
const express = require("express");
const bcrypt = require("bcrypt");
const Busboy = require("busboy");
const path = require("path");
const fs = require("fs");

const router = express.Router();

const { User, Post, Comment, File, addFile } = require("../src/db.js");
const { requiresLogin } = require("../src/util.js");

router.get("/login", (req, res) => res.render("login"));
router.get("/register", (req, res) => res.render("register"));

router.get("/logout", (req, res) => {
    req.session.destroy((err) => {
        console.log(err);
    });
    res.redirect("/?message=" + encodeURIComponent("Logged out successfully"));
});

router.get("/remove/:type/:id", requiresLogin, async (req, res) => {
    if(req.user.user === "admin") {
        return res.redirect("/?error=" + encodeURIComponent("Removing has been disabled for this user"));
    }

    const { type, id } = req.params;
    if(!id) {
        return res.redirect("/posts?error=" + encodeURIComponent("Missing id"));
    }

    let model;
    if(type === "file") model = File;
    else if(type === "post") model = Post;

    if(!model) {
        return res.redirect("/posts?error=" + encodeURIComponent("Invalid type to delete"));
    }

    let entry = await model.findByPk(id);
    if(!entry) {
        return res.redirect("/posts?error=" + encodeURIComponent("No item found with that id"));
    }
    if((await entry.getUser()).user !== req.user.user) {
        return res.redirect("/posts?error=" + encodeURIComponent("Cannot delete that item"));
    }

    res.render("remove", { type, id });
});

router.get("/file", async (req, res) => {
    let id = req.query.id;
    if(!id || typeof id !== "string") {
        return res.redirect("/?error=" + encodeURIComponent("No id provided"));
    }

    let entry = await File.findByPk(id);
    if(!entry) {
        return res.redirect("/?error=" + encodeURIComponent("A file was not found with that id"));
    }

    res.setHeader("Content-Type", entry.mimeType);
    res.setHeader("Content-Disposition", `inline; filename="${encodeURIComponent(entry.id)}"`);
    res.setHeader("Content-Length", fs.statSync("./uploads/" + entry.id).size);
    return fs.createReadStream("./uploads/" + entry.id).pipe(res);
});

router.post("/login", async (req, res) => {
    const { user, pass } = req.body;

    if(!user || !pass) {
        return res.redirect("/api/login?error=" + encodeURIComponent("Missing username or password"));
    }

    let entry = await User.findByPk(user);
    if(!entry) {
        return res.redirect("/api/login?error=" + encodeURIComponent("No user found with that username"));
    }

    if(!await bcrypt.compare(pass, entry.pass)) {
        return res.redirect("/api/login?error=" + encodeURIComponent("Incorrect password"));
    }

    req.session.user = user;
    res.redirect("/?message=" + encodeURIComponent("Logged in successfully"));
});

router.post("/register", async (req, res) => {
    const { user, pass } = req.body;
    if(!user || !pass) {
        return res.redirect("/api/register?error=" + encodeURIComponent("Missing username or password"));
    }

    if(await User.findByPk(user)) {
        return res.redirect("/api/register?error=" + encodeURIComponent("A user already exists with that username"));
    }

    try {
        await User.create({
            user,
            pass: await bcrypt.hash(pass, 12)
        });
    }
    catch(err) {
        return res.redirect("/api/register?error=" + encodeURIComponent(err.message));
    }

    req.session.user = user;
    return res.redirect("/?message=" + encodeURIComponent("Registered successfully"));
});

router.post("/create", requiresLogin, async (req, res) => {
    if(req.user.user === "admin") {
        return res.redirect("/?error=" + encodeURIComponent("Creating has been disabled for this user"));
    }

    const { title, text } = req.body;
    if(!title || !text) {
        return res.redirect("/profile?error=" + encodeURIComponent("Missing title or text"));
    }

    try {
        let post = await Post.create({
            title, text
        });
        req.user.addPost(post);
        post.setUser(req.user);
    }
    catch(err) {
        return res.redirect("/profile?error=" + encodeURIComponent(err.message));
    }
    return res.redirect("/profile?message=" + encodeURIComponent("Post created successfully"));
});

router.post("/remove", requiresLogin, async (req, res) => {
    if(req.user.user === "admin") {
        return res.redirect("/?error=" + encodeURIComponent("Creating has been disabled for this user"));
    }

    const { type, id } = req.body;
    if(!id || !type) {
        return res.redirect("/?error=" + encodeURIComponent("Missing id or type"));
    }

    let model;
    if(type === "file") model = File;
    else if(type === "post") model = Post;

    if(!model) {
        return res.redirect("/?error=" + encodeURIComponent("Invalid type to delete"));
    }

    let entry = await model.findByPk(id);
    if((await entry.getUser()).user !== req.user.user) {
        return res.redirect("/?error=" + encodeURIComponent("Cannot delete that item"));
    }
    await entry.destroy();

    if(type === "file") {
        await fs.promises.unlink(path.resolve("uploads", entry.id));

        if(req.user.profilePic.includes(entry.id)) {
            req.user.profilePic = null;
            await req.user.save();
        }
    }
    else if(type === "post") {
        for(let comment of await entry.getComments()) {
            await comment.destroy();
        }
    }

    res.redirect("/?message=" + encodeURIComponent(`The ${type} was deleted successfully`));
});

router.get("/comment/:id", requiresLogin, async (req, res) => {
    const { id } = req.params;
    if(!id) {
        return res.redirect("/posts?error=" + encodeURIComponent("Missing id"));
    }

    let post = await Post.findByPk(id);
    if(!post) {
        return res.redirect("/posts?error=" + encodeURIComponent("No post found with that id"));
    }

    if((await post.getUser()).user === "admin") {
        return res.redirect("/posts?error=" + encodeURIComponent("Sorry, commenting here has been disabled"));
    }

    res.render("comment", { id });
});

router.post("/comment", requiresLogin, async (req, res) => {
    let { id, text } = req.body;
    if(!id || !text) {
        return res.redirect("/?error=" + encodeURIComponent("Missing id or text"));
    }
    let post = await Post.findByPk(id);
    if(!post) {
        return res.redirect("/?error=" + encodeURIComponent("No post was found with that id"));
    }

    if((await post.getUser()).user === "admin") {
        return res.redirect(`/post/${id}?error=` + encodeURIComponent("Sorry, commenting here has been disabled"))
    }

    // no flags allowed!!! :>
    text = text.replace(/corctf{.*}/g, "[REDACTED]");

    try {
        let comment = await Comment.create({
            text
        });
        comment.setUser(req.user);
        comment.setPost(post);
        post.addComment(comment);
    }
    catch (err) { 
        return res.redirect(`/post/${id}?error=` + encodeURIComponent(err.message));
    }
    return res.redirect(`/post/${id}/?message=` + encodeURIComponent("Comment created successfully"));
});

router.get("/profilepic/:id", requiresLogin, async (req, res) => {
    if(req.user.user === "admin") {
        return res.redirect("/?error=" + encodeURIComponent("Changing the profile picture has been disabled for this user"));
    }

    let { id } = req.params;
    if(!id) {
        return res.redirect("/profile?error=" + encodeURIComponent("Missing id"));
    }
    let file = await File.findByPk(id);
    if(!file) {
        return res.redirect("/profile?error=" + encodeURIComponent("No file found with that id"));
    }
    if((await file.getUser()).user !== req.user.user) {
        return res.redirect("/profile?error=" + encodeURIComponent("You do not own that picture"));
    }
    req.user.profilePic = "/api/file?id=" + id;
    await req.user.save();
    return res.redirect("/profile?message=" + encodeURIComponent("Profile picture set successfully"));
});

router.post("/upload", requiresLogin, async (req, res) => {
    let busboy = new Busboy({ 
        headers: req.headers,
        limits: {
            fileSize: 100005, // 100 KB, but slightly over the limit 
                              // busboy truncates the file, but i don't even want it uploaded, so...
                              // we have it slightly over 100KB so addFile rejects it :)
            files: 1
        }
    });
    let chunks = [];
    let type;
    busboy.on('file', (fieldname, file, filename, encoding, mimetype) => {
        type = mimetype;
        file.on('data', (chunk) => chunks.push(chunk));
    });
    busboy.on('finish', function() {
        addFile(req.user, Buffer.concat(chunks), type).then(id => {
            res.redirect("/profile?message=" + encodeURIComponent("File uploaded successfully with id " + id));
        })
        .catch(err => {
            res.redirect("/profile?message=" + encodeURIComponent(err));
        });
    });
    req.pipe(busboy);
});

module.exports = router;
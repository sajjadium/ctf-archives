const express = require("express");
const router = express.Router();

const { Style, requiresLogin } = require("../src/db.js");

const createStylesheet = (style) => {
    if(style.url) {
        return `--styleme stylescript v1.0--
---------------
title: ${style.title}
url: ${style.url}
version: 1.0
---------------

${style.css}`;
    }
    else {
       return `--styleme stylescript v1.0--
---------------
title: ${style.title}
global: ${style.global || "false"}
version: 1.0
---------------

${style.css}`; 
    }
}

router.get("/mine", requiresLogin, async (req, res) => {
    res.render("list", {
        title: `${req.user.user}'s Styles`,
        styles: (await req.user.getStyles()).map(s => ({...s.toJSON(), code: createStylesheet(s)})),
        owner: true
    });
});

router.get("/search", async (req, res) => {
    let { query, user } = req.query;

    let styles = (await Style.findAll()).map(s => ({...s.toJSON()}));

    if(query) {
        query = query.toString().toLowerCase();
        styles = styles.filter(s => s.title.toLowerCase().startsWith(query)
                                    || s.id.toLowerCase().startsWith(query));
    }
    
    styles = styles.filter(s => s.hidden === false || req.isAdmin);
    if(user) {
        user = user.toString().toLowerCase();
        styles = styles.filter(s => s.UserUser === user);
    }

    // shuffle
    styles = [...styles].reduceRight((r,_,__,s) => (r.push(s.splice(0|Math.random()*s.length,1)[0]), r), []);
    // get first 8 styles
    styles = styles.slice(0, 8);

    styles = styles.map(s => ({...s, code: createStylesheet(s)}));
    res.render("list", { title: `Search Results:`, styles });
});

router.get("/i/:id", async (req, res) => {
    let { id } = req.params;
    let style = await Style.findByPk(id);

    if(!style) {
        req.session.error = "No style found with that id.";
        return res.redirect("/");
    }

    res.setHeader("Content-Type", "text/plain");
    res.send(createStylesheet(style));
});

module.exports = router;
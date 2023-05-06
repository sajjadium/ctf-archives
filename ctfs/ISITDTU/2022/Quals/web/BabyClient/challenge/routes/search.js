const express = require("express");

const router = express.Router();
const util = require("../src/util.js");


router.get("/", (req, res) => {
    res.render("search");
});

router.post("/", async (req, res) => {
    let query = `${req.body.query}%`;

    if(query) {
        return db.getEntry(query, util.isLocalhost(req))
			.then(entries => {
				if(entries.length == 0) {
                    util.flash(req, res, "error", "No results were found.");
                }
                else {
                    util.flash(req, res, "info", `${entries.length} search results found:`);
                }
			})

	}
	return res.status(403);
});

module.exports = router;
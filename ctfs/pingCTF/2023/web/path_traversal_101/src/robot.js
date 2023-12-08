export default (req, res, next) => {
    const userAgent = req.get("User-Agent");
    if (userAgent == "robot") {
        next();
    } else {
        res.render("robot", { error: "🤖🤖🤖🤖🤖" });
    }
};

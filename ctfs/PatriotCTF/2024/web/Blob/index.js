require("express")()
  .set("view engine", "ejs")
  .use((req, res) => res.render("index", { blob: "blob", ...req.query }))
  .listen(3000);

const express = require("express");
const axios = require("axios");
const fs = require("fs");
const path = require("path");
const { v4 } = require("uuid");

const app = express();
const uuid2ext = {};

function getFileName(uuid) {
  let ext = uuid2ext[uuid] ?? "";
  return uuid + ext;
}

app.set("view engine", "ejs");
app.use(express.urlencoded({extended: true}));
app.use("/photobucket", express.static("photobucket"));
app.use("/", express.static(__dirname + "/static"));

app.get("/", (req, res) => {
  res.render("index");
});

app.get("/uploadimage", (req, res) => {
  res.render("uploadimage.ejs");
});

app.post("/uploadimage", (req, res) => {
  const { url } = req.body;

  if (typeof url !== "string" || url === "")
    return res.render("uploadImage", { error: "Missing Image Url" });

  const imageID = v4();
  let fileExt = "." + url.split(".").pop();

  const imgExts = [".png", ".jpg", ".gif"];
  if (!imgExts.includes(fileExt)) fileExt = "";

  axios({
    method: "get",
    url: url,
    responseType: "stream",
  })
    .then(function (response) {
      response.data.pipe(
        fs.createWriteStream(`./photobucket/${imageID}${fileExt}`)
      );
      uuid2ext[imageID] = fileExt;
      res.redirect(`/image/${imageID}`);
    })
    .catch((error) => {
      console.log(error);
      res.render("uploadimage", { error: "Could not download image." });
    });
});

app.get("/image/:imageid", (req, res) => {
  let { imageid } = req.params;

  res.render("image", {
    imagelink: `photobucket/${getFileName(imageid)}`,
    image: imageid,
  });
});

app.get("/image/:imageid/download", (req, res) => {
  let { imageid } = req.params;

  res.sendFile(path.join(__dirname, `photobucket/${getFileName(imageid)}`));
});

app.listen(8080, async () => {
  fs.readFile("flag.txt", (err, data) => console.log(`Flag loaded!`));
});

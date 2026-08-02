import puppeteer from "puppeteer";
import { randomString, startFlagServer } from "./flag_server";
import express from "express";
import fileUpload from "express-fileupload";
import fs from "fs";

const runHTMLFile = async (filePath) => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(`file:${filePath}`);

  await page.evaluate(() => {
    const req = new window.XMLHttpRequest();
    req.open("GET", "http://localhost:6969/" + randomString, false);
    req.send(null);
  });
  const screenshot = await page.screenshot({
    path: filePath.replace(".html", ".png"),
    fullPage: true,
    type: "png",
  });
  await browser.close();

	return filePath.replace(".html", ".png");
};

const app = express();
app.use(fileUpload());
const port = 4242;
app.get("/", (req, res) => res.sendFile("index.html"));
app.get("/runHTML", async (req, res) => {
	// takes html file upload, saves it to "/uploads" + random string .html, runs it with the runHTMLFile function, and returns the screenshot
	const file = req.files.file;
	if (!file) {
		res.status(400).send("No file uploaded");
		return;
	}
	if (!file.mimetype.includes("html")) {
		res.status(400).send("File is not HTML");
		return;
	}

	const filePath = `/uploads/${Math.random().toString(36).substring(7)}.html`;
	fs.writeFileSync(filePath, file.data);
	const outputFilePath = runHTMLFile(filePath);
	res.sendFile(outputFilePath);
	// delete the files
	fs.rmSync(filePath);
	fs.rmSync(outputFilePath);
});

app.get('/sus.js', (req, res) => res.sendFile('sus.js'))

app.listen(port, () => console.log(`app listening on port ${port}!`));
startFlagServer();
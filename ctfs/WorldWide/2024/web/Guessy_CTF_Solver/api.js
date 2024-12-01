const express = require('express');
const { Browser } = require('happy-dom');
const app = express();
const port = process.env.PORT || 3000;
app.use(express.json());


const SOLVE_PATHS = ["robots.txt", "sitemap.xml"]
const prefix = /^[a-zA-Z]+$/
const easy_challenge = "https://fake-easy-chall.wwctf.com"

app.post('/hack', async (req, res) => {
    const url = req.body.url;
    const path = req.body.path || SOLVE_PATHS;
    const flagPrefix = req.body.flagPrefix || "wwf";
    console.log(req.headers)
    if (!flagPrefix.match(prefix)) {
        return res.status(400).json({ message: "I hack not you!!!" })
    }
    const flagRegex = new RegExp(`${flagPrefix}\\{.*?\\}`);

    if (url !== easy_challenge) {
        return res.status(400).json({ message: 'Hay i can only solve easy challenges!!' });
    }
    if (path.length > 3){
        return res.status(400).json({message: "Too many paths.."})
    }
    for (let i = 0; i < path.length; i++) {
        visit_url = new URL(path[i], easy_challenge);
        visit_url = visit_url.toString()
        try {
            const browser = new Browser();
            const page = browser.newPage();
            await page.goto(visit_url);
            const pageContent = page.mainFrame.document.body.innerHTML;
            const flag = pageContent.match(flagRegex);
            if (flag) {
                return res.json({ flag: flag[0] });
            }
        } catch (error) {
            console.error(error);
            return res.status(500).json({ message: 'Error fetching page' });
        }
    }
    return res.json({ message: 'Challenge is tough!!' });

});

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});

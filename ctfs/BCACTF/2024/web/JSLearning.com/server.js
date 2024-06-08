import express from 'npm:express@4.18.2'

const app = express();

const flag = Deno.readTextFileSync('flag.txt')

app.use(express.text())

app.use("/", express.static("static"));

app.post("/check", (req, res) => {

    let d = req.body;
    let out = "";
    for (let i of ["[", "]", "(", ")", "+", "!"]) {
        d = d.replaceAll(i, "");
    }
    if (d.trim().length) {
        res.send("ERROR: disallowed characters. Valid characters: '[', ']', '(', ')', '+', and '!'.");
        return;
    }

    let c;
    try {
        c = eval(req.body).toString();
    } catch (e) {
        res.send("An error occurred with your code.");
        return
    }

    // disallow code execution
    try {
        if (typeof (eval(c)) === "function") {
            res.send("Attempting to abuse javascript code against jslearning.site is not allowed under our terms and conditions.");
            return
        }
    } catch (e) {}


    out += "Checking the string " + c + "...|";
    if (c === "fun") {
        out+='Congratulations! You win the level!';
    } else {
        out+="Unfortunately, you are incorrect. Try again.";
    }
    res.send(out);
});

const server = app.listen(0, () => console.log(server.address().port))

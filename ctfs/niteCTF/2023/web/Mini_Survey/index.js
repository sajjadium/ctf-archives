const express = require("express");
const updateDBs = require("./serverComs");

PORT = process.argv[2];
if (!PORT) {
    console.log("Enter port");
    process.exit();
}

const app = express();

app.set("view engine", "ejs");
app.use(express.urlencoded({ extended: true }));

//add initial data as headers to convert to csv
let surveyOneInitialData = { Name: { City: "Rating" } };
let surveyTwoInitialData = { Name: { City: { Rating: "Reasons" } } };

app.get("/", (req, res) => {
    res.render("home");
});

app.get("/pollutionsurvey", (req, res) => {
    res.render("pollution");
});

app.get("/roadqualsurvey", (req, res) => {
    res.render("roadqual");
});

app.post("/roadqualsurvey", (req, res) => {
    console.log(23);
    const fieldInput1 = req.body.name;
    const fieldInput2 = req.body.city;
    const fieldInput3 = req.body.roadRate;
    const fieldInput4 = req.body.reasons;

    let reasons = fieldInput4.split(",");

    surveyTwoInitialData[fieldInput1] = {
        [fieldInput2]: { [fieldInput3]: reasons },
    };

    console.log(surveyTwoInitialData);

    test = Object.create(surveyTwoInitialData);
    console.log(test.url);

    surveyTwoInitialData = updateDBs(surveyTwoInitialData, {
        Name: { City: { Rating: "Reasons" } },
    });

    res.redirect("/thankyou");
});

app.post("/pollutionsurvey", (req, res) => {
    let fieldInput1 = req.body.name;
    let fieldInput2 = req.body.city;
    let fieldInput3 = req.body.pollutionRate;

    surveyOneInitialData[fieldInput1] = { [fieldInput2]: fieldInput3 };

    surveyOneInitialData = updateDBs(surveyOneInitialData, {
        Name: { City: "Rating" },
    });

    res.redirect("/thankyou");
});

app.get("/thankyou", (req, res) => {
    res.render("thankyou");
});

console.log(`Listening at http://localhost:${PORT}`);
app.listen(PORT);

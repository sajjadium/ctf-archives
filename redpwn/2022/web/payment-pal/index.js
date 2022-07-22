const express = require("express");

const app = express();

const PORT = process.env.PORT || 8080;

app.use(require("cookie-parser")());
app.use(express.static("public"));
app.use("/graphql", require("./src/graphql.js"));

app.listen(PORT, () => console.log(`web/payment-pal listening on port ${PORT}`));
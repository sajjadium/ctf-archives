const express = require('express');
const session = require('express-session');
require('dotenv').config();

const app = express();
const port = 3000;

const FLAG = process.env.FLAG;

app.use(session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: true,
    cookie: { maxAge: 24 * 60 * 60 * 1000 } // 24 hours
}));

// Middleware to check if user session exists
const checkUserSession = (req, res, next) => {
    if (!req.session.user) {
        req.session.user = {
            debtAmount: 0,
            gold: 0,
            swampShade: false,
            loanPending: false
        };
    }
    next();
};
app.use(checkUserSession);

function verifyAmount(gold) {
    gold = parseInt(gold);
    if (isNaN(gold) || gold < 1) {
        return false;
    }
    return true;
}

// Map Potion ID to Name and Price
const potions = [
    { name: "Essence of the Abyss ⚗️", price: 10 },
    { name: "Potion of Astral Alignment ⚗️", price: 2 },
    { name: "Elixir of the Enigma ⚗️", price: 34 },
    { name: "Stardust Elixir 🧪", price: 11 },
    { name: "Swampshade Serum ⚗️", price: 100 },
    { name: "Phoenix Tears Potion ⚗️", price: 65 },
];

app.get('/stats', (req, res) => {
    // Show current stats
    res.json({
        debtAmount: req.session.user.debtAmount,
        gold: req.session.user.gold,
        swampShade: req.session.user.swampShade,
        loanPending: req.session.user.loanPending
    });
});

app.get('/checkout', (req, res) => {
    // Check if user has a pending loan
    if (req.session.user.loanPending) {
        return res.json({ message: "Ermm you still have a debt 🤓" });
    }

    // Set the loan to pending
    if (req.session.user.swampShade) {
        return res.json({ message: "You are worthy: " + FLAG });
    }
    else {
        return res.json({ message: "You don't possess the SwampShade potion!" });
    }
});

// Example request: http://localhost:3000/borrow?amount=1000
app.get('/borrow', (req, res) => {
    let amount = req.query.amount;
    // Check if request is a number
    if (!verifyAmount(amount)) {
        return res.json({ message: "Invalid amount" });
    }

    if (req.session.user.loanPending) {
        return res.json({ message: "Repay your loan first!" });
    } else {
        // Set the loan to pending
        req.session.user.loanPending = true;
        req.session.user.debtAmount = Number(amount);
        req.session.user.gold = Number(amount);
        return res.json({ message: "You have successfully borrowed gold 🪙" });
    }

});

// Example request: http://localhost:3000/buy?id=1
app.get('/buy', (req, res) => {
    potionID = req.query.id;
    // Check if potion ID is valid
    if (!potionID || !potions[potionID]) {
        return res.json({ message: "Invalid potion ID" });
    }

    // Buy the potion
    if (req.session.user.gold < potions[potionID].price) {
        return res.json({ message: "Not enough gold" });
    }

    // Update user's stats
    req.session.user.gold -= potions[potionID].price;
    // SwampShade Serum
    if (potionID == 4) {
        req.session.user.swampShade = true;
    }
    return res.json({ message: "Potion acquired" });
});


// Example request: http://localhost:3000/repay?amount=1000
app.get('/repay', checkUserSession, (req, res) => {

    // Get the amount to be repayed
    let amount = req.query.amount;

    // Check if user has a pending loan
    if (!req.session.user.loanPending) {
        return res.json({ message: "You do not have any debts" });
    }

    // Check if request is a number
    if (!verifyAmount(amount)) {
        return res.json({ message: "Invalid amount" });
    }

    // If the amount is a number, check if it's enough to repay the loan
    if (req.session.user.gold < Number(amount)) {
        return res.json({ message: "You don't have that much money" });
    }

    // Check if the amount is enough to repay the loan
    if (req.session.user.debtAmount <= Number(amount)) {
        return res.json({ message: "This is not enough to repay the debt" });
    }

    // Repay the loan
    req.session.user.gold = 0;
    req.session.user.debtAmount = 0;
    req.session.user.loanPending = false;

    return res.json({ message: "✨ Debt Repaid ✨" });
});


app.get('/', (req, res) => {
    res.json({ message: "My potions are too expensive for you, traveler! 🧙" });
});

app.listen(port, () => {
    console.log(`App listening at http://localhost:${port}`);
});
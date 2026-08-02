import { BankClass } from "../modules/bank.js";

// using ip accounts for now
const bank = new BankClass();
// provisional ddos protection
let uses = 0;

const funds = {
    litlit: {
        name: "Lit LIT Fund",
        desc: "Make LIT LIT!!!",
        goal: 9999.99,
        raised: 14739.59,
        image: "https://lit.lhsmathcs.org/image/originalLogo.png",
    },
    codetigerorz: {
        name: "CodeTiger Orz Fund",
        desc: "Support the efforts to orz CodeTiger orz",
        goal: 90071992547409.91,
        raised: 19904745299170.09,
        image: "https://media.discordapp.net/stickers/1029206417372094485.webp",
    },
    flag: {
        name: "Flag-ship Fund",
        desc: "Special surprise when we reach our funding goal!",
        goal: 0.50,
        raised: 0.00,
        image: "https://upload.wikimedia.org/wikipedia/commons/5/5d/White_flag_icon.svg",
    },
};

// keep these secret!
const messages = {
    litlit: "Order to purchase 999 torches confirmed",
    codetigerorz: "orzosity",
    flag: "[FLAG]",
};

for (const [fund, props] of Object.entries(funds)) {
    if (props.raised >= props.goal) {
        props.message = messages[fund];
    }
}

const error = (rep, message) => {
    rep.code(400);
    return {
        statusCode: 400,
        error: "Bad Request",
        message,
    };
};

export default async (fastify) => {
    fastify.get("/balance", async (req, rep) => {
        return { money: await bank.getMoney(req.ip) };
    });

    fastify.get("/funds", async (req, rep) => {
        return funds;
    });

    fastify.post("/donate",
        {
            schema: {
                body: {
                    type: "object",
                    properties: {
                        fund: { type: "string" },
                        amount: { type: "number" },
                    },
                    required: ["fund", "amount"],
                },
            },
        },
        async (req, rep) => {
            const { fund, amount } = req.body;

            // validation
            if (!Object.hasOwn(funds, fund)) {
                return error(rep, "fund does not exist");
            }
            if (amount <= 0) {
                return error(rep, "donation must be positive");
            }
            if (amount > funds[fund].goal) {
                return error(rep, "can't process such a large donation");
            }
            if (amount !== +amount.toFixed(2)) {
                return error(rep, "donation cannot have fractional cents");
            }
            if (uses > 50) {
                return error(rep, "too many donations being processed, please try again later");
            }
            ++uses;

            // who implemented this stupid bank class???
            const money = await bank.addMoney(req.ip, -amount);
            // have to do this since otherwise this will take twice as long for valid requests
            if (money < 0) {
                await bank.addMoney(req.ip, amount);
                return error(rep, "not enough money in account");
            }

            // success!
            funds[fund].raised += amount;
            if (funds[fund].raised >= funds[fund].goal) {
                funds[fund].message = messages[fund];
            }
            return {
                money,
            };
        },
    );
};

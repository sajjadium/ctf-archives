const vm = require(`vm`);
const Discord = require(`discord.js`);
const client = new Discord.Client();

const { secret } = require(`./secrets.js`);

const responses = {
    greeting: [`Hello there!`, `Hi! Nice to meet you!`, `Hello!`, `Hi there!`],
    condition: [`I'm fine, thanks!`, `I'm good.`, `I'm doing awesome!`, `I'm doing well, thank you!`],
    farewell: [`Bye bye!`, `Goodbye!`, `Fare thee well!`, `Until next time!`],
    generic: [`Wonderful weather we're having!`, `I like ice cream.`, `Pineapples shouldn't be on pizza.`, `I'd like to visit the Moon some day.`,
              `Cats are awesome.`, `I like to play sandbox games.`, `Prussian blue is my favorite color.`],
    secret: secret
};

const sanitize = (str) =>
{
    if(/gimme secret/i.test(str))
    {
        str = str.replace(/gimme secret/i, ``);
        return sanitize(str);
    }
    return str;
};

const fetchResponse = (responseType) =>
{
    return responses[responseType][Math.floor(Math.random() * responses[responseType].length)];
};

const lower = (str) => { return str.toLowerCase(); };
const upper = (str) => { return str.toUpperCase(); };

client.on(`message`, (msg) =>
{
    let user = msg.author;
    if(msg.channel.type != `dm` || user == client.user) return;
    let content = msg.content.replace(/\d+/g, ``);

    try
    {
        content = lower(vm.runInContext(`"${lower(sanitize(content))}"`, vm.createContext({lower: lower, upper: upper})));
    } catch(err) {
        content = ``;
    }

    if(content.startsWith(`hi`) || content.startsWith(`hello`) || content.startsWith(`hey`))
    {
        user.send(fetchResponse(`greeting`));
    } else if(content.startsWith(`how are you`) || content.startsWith(`hru`)) {
        user.send(fetchResponse(`condition`));
    } else if(content.startsWith(`bye`)) {
        user.send(fetchResponse(`farewell`));
    } else if(content == `gimme secret`) {
        user.send(fetchResponse(`secret`));
    } else {
        user.send(fetchResponse(`generic`));
    }
});

client.login(process.env.BOT_TOKEN);

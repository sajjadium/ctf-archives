const ffmpeg = require('fluent-ffmpeg');
const { Readable } = require('stream');
const Discord = require('discord.js');
const fetch = require('node-fetch');
const math = require('mathjs');
const url = require('url');

const PREFIX = "f!";

const API = "http://192.168.0.6:8000";
// const API = "http://localhost:8000";

let client = new Discord.Client();
let data = new Map();

let newEmbed = () => {
    let template = new Discord.MessageEmbed()
        .setColor('#0099ff')
        .setTitle('FlagBot')
        .setTimestamp();
    return template;
};

const play = (id) => {
    let info = data.get(id);
    return new Promise((resolve, reject) => {
        fetch(`${API}/ytdl`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ id: info.id })
        }).then(async res => {
            let song = await res.buffer();
            ffmpeg.ffprobe(Readable.from(song), async (err, data) => {
                if(err) {
                    console.log(err);
                    return resolve(false);
                }
                info.duration = data.format.duration;
                let dispatcher = (await info.vc.join()).play(Readable.from(song));
                dispatcher.on("finish", () => resolve(true));
                dispatcher.on("error", () => resolve(false));
            });
        }).catch(async (err) => {
            console.log(err);
            resolve(false);
        });
    });
};

// a lot of this extra code is just to make sure the bot looping the song doesn't die
const loop = async (id) => {
    let info = data.get(id);
    let counter = 0;
    while(info.looping) {
        await Promise.any([
            play(id),
            new Promise((resolve, reject) => {
                data.get(id).duration ? setTimeout(resolve, data.get(id).duration * 1500) : reject(0);
            })
        ]);
        counter++;

        // just some fix to disconnect / reconnect so bot doesn't lose connection
        if(counter % 20 === 0) {
            counter = 0;
            info.vc.leave();
            await new Promise((resolve, reject) => setTimeout(resolve, 5000));
        }

        await new Promise((resolve, reject) => setTimeout(resolve, 3000));
    }
};

const disconnect = async (id) => {
    let info = data.get(id);
    if(info) {
        info.vc.leave();
    }
    data.delete(id);
};

client.on('ready', async () => {
    console.log(`[BOT] Logged in as ${client.user.tag}!`);
    client.user.setActivity(`${PREFIX}help`);

    let vc = await client.channels.fetch("856790442037608448");
    let info = {
        id: "[redacted]",
        vc,
        looping: true,
        guild: vc.guild.id
    };
    data.set(info.guild, info);
    loop(info.guild);
});

client.on('message', async (msg) => {
    if(msg.content.startsWith(PREFIX)) {
        let content = msg.content.slice(PREFIX.length);
        let args = content.split(" ");
        let cmd = args[0];

        // must have "flagbot" role!!!!
        let isOwner = msg.guild
            && msg.channel.type === "text"
            && msg.member.roles.cache.find(r => r.name === /*"Server Booster*/ "flagbot");

        // must be a bot author :)
        //              Strellic               FizzBuzz101
        let isAuthor = ["140239296425754624", "480599846198312962"].includes(msg.author.id);

        if(cmd === "help") {
            let embed = newEmbed()
                .setDescription("List of commands:")
                .addField(`${PREFIX}help`, `Shows you this menu.`)
                .addField(`${PREFIX}ping`, `Shows the ping of the bot.`)
                .addField(`${PREFIX}coinflip`, `Flips a coin.`)
                .addField(`${PREFIX}8ball`, `Answers your questions.`)
                .addField(`${PREFIX}math`, `Evaluates a math expression. [OWNER ONLY]`)
                .addField(`${PREFIX}status`, `Checks whether a website is online. [OWNER ONLY]`)
                .addField(`${PREFIX}play`, `Play song from YouTube. [AUTHOR ONLY]`)
                .addField(`${PREFIX}loop`, `Loop song from YouTube. [AUTHOR ONLY]`)
                .addField(`${PREFIX}stop`, `Stop currently playing song. [AUTHOR ONLY]`);

            msg.reply(embed);
        }
        else if(cmd === "ping") {
            let embed = newEmbed()
                .setDescription("Current Ping:")
                .addField("Ping:", `${Date.now() - msg.createdTimestamp} ms`);
            msg.reply(embed);
        }
        else if(cmd === "coinflip") {
            let isHeads = Math.random() < 0.5;
            let embed = newEmbed()
                .setDescription("Coinflip")
                .setImage(isHeads ? "https://i.imgur.com/rmEsT0V.png" : "https://i.imgur.com/jYgByVa.png")
                .addField("You got:", isHeads ? "Heads" : "Tails");
            msg.reply(embed);
        }
        else if(cmd === "8ball") {
            if(args.length < 2) {
                return msg.reply(`usage: ${PREFIX}8ball <question>`)
            }

            let question = args.slice(1).join(" ");
            let responses = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes – definitely', 'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Yes Signs point to yes', 'Reply hazy', 'try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Dont count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful'];

            if(!question.endsWith("?"))
                question += "?"

            let embed = newEmbed()
                .setDescription("8-Ball")
                .addField(question, responses[Math.floor(Math.random() * responses.length)]);

            msg.reply(embed);
        }
        else if(cmd === "math") {
            if(!isOwner) {
                return msg.reply("you are not the bot's owner!");
            }
            if(args.length < 2) {
                return msg.reply(`usage: ${PREFIX}math <expression>`);
            }

            let expr = args.slice(1).join(" ");
            let embed = newEmbed();
            try {
                // mathjs not in scope for this challenge...
                embed.addField("**Math**", `${expr} = ${math.evaluate(expr)}`);
            }
            catch {
                embed.addField("**Math**", `There was an error evaluating your expression.`);
            }

            msg.reply(embed);
        }
        else if(cmd === "status") {
            if(!isOwner) {
                return msg.reply("you are not the bot's owner!");
            }

            fetch(API + "/check", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ url: args.slice(1).join(" ") })
            }).then(r => r.text()).then(r => {
                return msg.reply("the site is probably up or down, not sure? maybe you could check f!8ball lol");
            })
            .catch(err => {
                return msg.reply(`there was an error checking for the website status!`);
            });
        }
        else if(cmd === "play" || cmd === "loop") {
            if(!isOwner) {
                return msg.reply("you are not the bot's owner!");
            }
            if(!isAuthor) {
                return msg.reply("you are not the bot's author!");
            }

            let yt = args[1];
            if(!yt || !yt.includes("youtube.com/watch?v=")) {
                return msg.reply(`usage: ${PREFIX}${cmd} <youtube url> [vc id]`);
            }

            let id = url.parse(yt, true).query.v;
            if(!id || !/^[a-zA-Z0-9-_]{11}$/.test(id)) {
                return msg.reply("invalid youtube url");
            }

            let vc;
            if(args[2]) {
                vc = await client.channels.fetch(args[2]);
            }
            else {
                vc = msg.member.voice.channel;
            }

            if(!vc || vc.type !== "voice") {
                return msg.reply(`no voice channel to join!`);
            }

            let info = {
                id,
                vc: vc,
                looping: cmd === "loop",
                guild: vc.guild.id
            };
            data.set(info.guild, info);

            if(info.looping) {
                loop(info.guild);
            }
            else {
                await play(info.guild);
                disconnect(info.guild);
            }
        }
        else if(cmd === "stop") {
            if(!isOwner) {
                return msg.reply("you are not the bot's owner!");
            }
            if(!isAuthor) {
                return msg.reply("you are not the bot's author!");
            }

            let id = args[1] || msg.guild.id;
            let info = data.get(id);
            if(info) {
                info.looping = false;
                disconnect(id);
                return msg.reply("bye bye!");
            }
            else {
                return msg.reply("not currently playing anything???");
            }
        }
    }
});

client.login(process.env.TOKEN);

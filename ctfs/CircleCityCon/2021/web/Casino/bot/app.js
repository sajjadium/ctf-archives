import Discord from 'discord.js'
import fetch from 'node-fetch'
import puppeteer from 'puppeteer'

const prefix = '$'
const client = new Discord.Client()
const apiUrl = 'http://172.16.0.10:3000'

let browser

client.once('ready', async () => {
  browser = await puppeteer.launch({
    pipe: true,
    dumpio: true,
    args: [
      '--disable-dev-shm-usage', // Docker stuff
      '--js-flags=--jitless' // No Chrome n-days please
    ]
  })
  console.log('Ready')
})

async function addUser (user) {
  return await fetch(
    `${apiUrl}/add_user?${new URLSearchParams({
      user: user.tag,
      avatar: user.avatarURL()
    })}`
  )
}

async function getBalance (user) {
  const res = await fetch(
    `${apiUrl}/balance?${new URLSearchParams({ user: user.tag })}`
  )
  const balance = await res.json()
  return res.status === 200 ? balance : undefined
}

async function setBalance (user, balance) {
  return await fetch(
    `${apiUrl}/set_balance?${new URLSearchParams({
      user: user.tag,
      balance
    })}`
  )
}

function getRandomInt (min, max) {
  min = Math.ceil(min)
  max = Math.floor(max)
  return Math.floor(Math.random() * (max - min) + min)
}

async function balance (message) {
  const user = message.author
  let balance = await getBalance(user)
  if (balance === undefined) {
    addUser(user)
    balance = 0
  }

  message.channel.send(`You have $${balance}`)
}

async function beg (message) {
  const user = message.author
  let balance = await getBalance(user)
  if (balance === undefined) {
    addUser(user)
    balance = 0
  }

  if (balance >= 100) {
    return message.channel.send('No')
  }

  const donation = getRandomInt(1, 100)
  balance += donation
  await setBalance(user, balance)
  message.channel.send(
    `Ok fine I donated $${donation}, you now have $${balance}`
  )
}

async function bet (message, bet) {
  const user = message.author
  let balance = await getBalance(user)
  if (balance === undefined || balance < 0) {
    return message.channel.send('You literally have no money')
  }

  if (bet.length === 0) {
    return message.channel.send('You need to tell me how much to bet')
  }

  bet = bet.startsWith('$') ? bet.slice(1) : bet
  bet = parseInt(bet)
  if (isNaN(bet) || bet <= 0 || bet > balance) {
    return message.channel.send('No')
  }

  const yourDice = getRandomInt(1, 6 + 1)
  let myDice = getRandomInt(1, 6 + 1)

  // Avert your eyes
  if (balance + bet >= 1000) myDice = 6

  const lines = [`You rolled a ${yourDice} and I rolled a ${myDice}`]

  if (yourDice > myDice) {
    balance += bet
    await setBalance(user, balance)
    lines.push(`Congrats you won $${bet}`)
    lines.push(`You now have $${balance}`)
  } else if (yourDice < myDice) {
    balance -= bet
    await setBalance(user, balance)
    lines.push(`Haha idiot you just lost $${bet}`)
    lines.push(`You now have $${balance}`)
  } else {
    lines.push('Tie')
  }

  message.channel.send(lines.join('\n'))
}

async function rich (message) {
  const res = await fetch(`${apiUrl}/rich`)
  const rich = await res.json()
  const lines = rich.map((p) => `**${p.user}** $${p.balance}`)
  message.channel.send(lines.join('\n'))
}

const cooldown = 5000 // Cooldown betwen requesting badges in milliseconds
const cooldownTable = {} // Users -> last time requested

async function badge (message, css) {
  const user = message.author

  const now = new Date().getTime()
  if (user.tag in cooldownTable && now - cooldownTable[user.tag] < cooldown) {
    message.channel.send('Slow it down')
    return
  } else {
    cooldownTable[user.tag] = now
  }

  let balance = await getBalance(user)
  if (balance === undefined) {
    addUser(user)
    balance = 0
  }

  if (css.startsWith('```css') && css.endsWith('```')) {
    css = css.slice(6, -3).trim()
  } else if (css.startsWith('```') && css.endsWith('```')) {
    css = css.slice(3, -3).trim()
  } else if (css.startsWith('`') && css.endsWith('`')) {
    css = css.slice(1, -1).trim()
  }

  message.channel.startTyping()
  const ctx = await browser.createIncognitoBrowserContext()
  const page = await ctx.newPage()

  try {
    await page.goto(
      `${apiUrl}/badge?${new URLSearchParams({ user: user.tag, css })}`,
      { waitUntil: 'networkidle2' }
    )

    const badge = await page.waitForSelector('#badge')
    const screenshot = await badge.screenshot()

    message.channel.send({ files: [screenshot] })
    message.channel.stopTyping()
  } catch (e) {
    message.channel.send('Error generating badge')
  } finally {
    await page.close()
    await ctx.close()
  }
}

async function flag (message) {
  const balance = await getBalance(message.author)
  if (balance === undefined || balance < 1000) {
    message.channel.send('You need at least $1000 to get the flag, peasant')
  } else {
    message.channel.send(`Here you go: \`${process.env.FLAG}\``)
  }
}

async function help (message) {
  const msg = `Website: ${process.env.PUBLIC_URL}
\`\`\`
${prefix}balance
${prefix}beg
${prefix}bet
${prefix}rich
${prefix}badge
${prefix}flag
\`\`\``
  message.channel.send(msg)
}

client.on('message', async (message) => {
  if (!message.content.startsWith(prefix) || message.author.bot) return

  // Split command and arg on first space because parsing is hard
  // Example: "!cmd foo bar baz" -> "cmd", "foo bar baz"
  // Example: "!cmd" -> "cmd", ""
  let command = message.content.slice(prefix.length).trim()
  let arg = ''
  const split = command.indexOf(' ')
  if (split > 0) {
    arg = command.slice(split + 1)
    command = command.slice(0, split)
  }

  if (command === 'help') {
    await help(message)
  } else if (command === 'balance') {
    await balance(message)
  } else if (command === 'beg') {
    await beg(message)
  } else if (command === 'bet') {
    await bet(message, arg)
  } else if (command === 'rich') {
    await rich(message)
  } else if (command === 'badge') {
    if (message.channel.type === 'dm') {
      await badge(message, arg)
    } else {
      message.channel.send('Talk to me in DM')
    }
  } else if (command === 'flag') {
    if (message.channel.type === 'dm') {
      await flag(message)
    } else {
      message.channel.send('Talk to me in DM')
    }
  } else {
    message.channel.send("That command doesn't even exist")
  }
})

client.login(process.env.DISCORD_TOKEN)

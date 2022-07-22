const crypto = require('crypto');
const puppeteer = require('puppeteer');
let queue = [];
let running = false;

function getRandomFlag() {
	return "flag{" + crypto.randomBytes(8).toString("hex") + "}";
}

function verifyFlag(flags,users,flag,user) {
	if(flag in flags) {
		var flagger = flags[flag][0];
		var ogOwner = flags[flag][1];
		delete flags[flag];

		var tmpIndex = users[ogOwner]["owns"].indexOf(flagger);
		if(tmpIndex >= 0) users[ogOwner]["owns"].splice(flagger,1);

		users[user]["owns"].push(flagger);
		var f = getRandomFlag();
		flags[f] = [flagger,user];
		users[flagger]["flag"] = f;
	}
}

// Runs about every 5 minutes

async function run(secretCode,flags,users) {
	let browser;

	try {
		if(running) return;
		module.exports.running = true;
		console.log("Running bot!");

		// Randomly Shuffle the queue
		for (var i = queue.length - 1;i > 0;--i) {
			var j = Math.floor(Math.random() * (i + 1));
			var temp = queue[i];
			queue[i] = queue[j];
			queue[j] = temp;
		}

		browser = await puppeteer.launch({
			headless: true,
			pipe: true,
			args: ['--incognito', '--no-sandbox', '--disable-setuid-sandbox'],
			slowMo: 10
		});

		let page = (await browser.pages())[0];

		await page.goto('http://localhost:8080/register');
		var adminUsername = crypto.randomBytes(8).toString('hex');
		await page.type('[name="username"]', adminUsername);	
		await page.type('[name="password"]', secretCode);


		await Promise.all([
			page.click('[type="submit"]'),
			page.waitForNavigation({ waituntil: 'domcontentloaded' })
		]);

		users[adminUsername]["owns"].length = 0;
		users[adminUsername]["admin"] = true;

		while(queue.length > 0) {
			var curUser = queue.pop();
			// console.log("Processing " + curUser);
			if(users[curUser].disabled) continue;
			await page.goto('http://localhost:8080/view/' + curUser);
			await page.waitForTimeout(5000);
			let element = await page.$('#totalFlags');
			let count = !element ? 0 : await page.evaluate(el => el.textContent, element);
			count = parseInt(count) || 0;
			// A person should not have more than 100 flags :skull:
			count = Math.min(count,100);
			// Clear original owns
			users[curUser]["owns"].length = 0;
			for(var i = 1;i <= count;++i) {
				let element = await page.$('#flag-' + i);
				let curFlag = !element ? "" : await page.evaluate(el => el.textContent, element);
				if(!curFlag) {
					break;
				}
				verifyFlag(flags,users,curFlag,curUser);
			}
			var systemMsg = "The admin bot has processed your request, and you now have " + users[curUser]["owns"].length + " flag(s), and these are your new flags:<br>";
			for(var i = 0;i < users[curUser]["owns"].length;++i) {
				var curFlagger = users[curUser]["owns"][i];
				systemMsg += curFlagger + " : " + users[curFlagger]["flag"] + "<br>";
			}
			users[curUser]["system"] = systemMsg;
			users[curUser]["querying"] = false;
		}

		await browser.close();
	} catch(e) {
		console.error(e);
		try { await browser.close() } catch(e) {}
	}

	module.exports.running = false;	

}

module.exports = { running, queue, run }

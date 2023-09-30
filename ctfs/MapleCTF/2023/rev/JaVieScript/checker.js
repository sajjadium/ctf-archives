var flag = "maple{";
var honk = {};

async function hash(string) {
	const utf8 = new TextEncoder().encode(string);
	const hashBuffer = await crypto.subtle.digest('SHA-256', utf8);
	const hashArray = Array.from(new Uint8Array(hashBuffer));
	const hashHex = hashArray
	  .map((bytes) => bytes.toString(16).padStart(2, '0'))
	  .join('');
	return hashHex;
  }

async function constructflag() {
	const urlParams = new URLSearchParams(window.location.search);
	var fleg = "maple{";
	for (const pair of urlParams.entries()) {
		honk[pair[0]] = JSON.parse(pair[1]); 
	}

	if (honk.toString() === {}.toString()) {
		fleg += honk.toString()[9];
	}

	if (Object.keys(honk).length === 0) {
		const test = eval(honk.one);
		if (typeof test === 'number' && test * test + '' == test + '' && !/\d/.test(test)) {
			fleg += 'a' + test.toString()[0];
		}

		const quack = honk.two;

		if (quack.toString().length === 0 & quack.length === 1) {
			fleg += 'a' + (quack[0] + '')[0].repeat(4) + 'as';
		}

		const hiss = honk.three;

		if (hiss === "_are_a_mId_FruiT}") {
			fleg += hiss;
		}
	}
	if (await hash(fleg) == "bfe06d1e92942a0eca51881a879a0a9aef3fe75acaece04877eb0a26ceb8710d") {
		console.log(fleg);
	}
}

constructflag();

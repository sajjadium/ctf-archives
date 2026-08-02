const xml2js = require("xml2js");
var forbiddenDictionary;

class fanfic {
	constructor(name,parent) {
		this.name = name;
		this.parent = parent;
		this.text = "";
		this.root = false;
		this.literals = [];
	}

	get getChild() {
		return this.child;
	}

	toString() {
		if(this.text) return this.text;
		return this.name;
	}
}

var literals = ["eyangstory1","eyangstory2","eyangstory3"];

function generateLiteral(literal) {
	if(literal == literals[0]) {
		return "In the vast expanse of the coding universe, I was just another programmer, skilled but ordinary. My days were filled with lines of code and tech challenges, but my heart held a secret—a hidden spark of admiration for a legendary figure known as EyangCH. Oh, how I longed to meet him, to learn from the best and bask in the glow of his brilliance! He seemed to excel at everything he touched, from coding to solving the most complex algorithms. Each day, I struggled with a dilemma that seemed to tear me apart. In the familiar realm of coding, I thrived, gaining recognition and praise. But the thought of reaching out to EyangCH left me paralyzed with anxiety. Doubts haunted my every step—What if he brushed me off? What if I wasn't good enough for his attention? Then, one fateful night, as I delved deep into a coding challenge, I stumbled upon a hidden message from EyangCH in a cryptic forum. The words were like a beacon of hope, encouraging me to keep pushing myself and not be afraid of my own greatness. It was a sign, a gentle nudge from destiny, pushing me to take that leap of faith. Summoning the courage, I decided to reach out to EyangCH, but I opted for anonymity at first. I initiated a conversation, discussing coding, inspirations, and challenges without revealing my true identity. And much to my surprise, he responded warmly, sharing his wisdom and experiences, oblivious to my true identity. As days turned into weeks, our friendship flourished in the shadows of anonymity. EyangCH eventually invited me to a virtual meet-up of like-minded coders. My heart pounded with excitement and nervousness. Should I reveal myself? Would he accept me, a mere admirer, into his circle of brilliance? The day of the meet-up arrived, and my mind was clouded with indecision. I yearned to be known as more than just an anonymous admirer, yet I feared the potential rejection that loomed on the horizon. With trembling hands, I took a deep breath and typed my real name, baring my soul and my story. I confessed how much he meant to me, how he had been my guiding light in the vast sea of coding. And then I waited, my heart pounding like an ancient drum, anticipating the moment of truth. Minutes that felt like hours passed until a reply appeared from EyangCH. To my astonishment, he responded warmly, thanking me for my kind words and expressing gratitude for the connection we had formed. Tears of relief and joy welled up in my eyes as the weight of fear lifted from my shoulders. From that moment on, our friendship blossomed beyond the boundaries of coding. We conquered challenges together, exchanged ideas, and supported each other through highs and lows. The shadows of admiration transformed into a shining bond that would endure through the ever-changing currents of the coding universe. In the realm of coding, where lines of code danced like fireflies, a friendship had bloomed—an extraordinary tale of how an admirer found the courage to reveal himself and stand tall beside his idol, EyangCH. Our journey together continued, with a newfound sense of confidence and camaraderie that would forever light the path ahead.";
	}else if(literal == literals[1]) {
		return "I’m telling you, EyangCH is as cracked as he is jacked. Saw him the other day benching 696lbs while wearing plot armor for life. I asked him what he was doing and he said 'better than you' and walked out with a explosion. Later on I saw him in a cafeteria working with benq to propose some innovative problems. When I commented on how high quality they were, EyangCH just nodded slightly and went back to inventing quantum computing. When I was first in line to buy state of the art EyangCH quantum computers, EyangCH gave me a small discount, but as I expressed my gratitude, he walked away and adjusted his plot armor.";
	}else{
		return "“Winning isn’t everything, it’s the only thing”- Nelson Mandela. The story of EyangCH always intrigued me; how could this person be on top of the competitive programming world for what seems like forever? From his first AK IOI, to his now consecutive ICPC World Finalists -1th place medal and countless achievements between, not only was his talent timeless, but his effort as well. It must have been an effort which overcame every tribulation, broke every obstacle, the tireless stampede of a genius climbing Olympus Mons, while other top competitors lolled on Everest. ";
	}
}


function addDefinition(node,def) {
	if(def['$']['text']) {
		node.text = String(def['$']['text']);
	}
	if(def['$']['prefix']) {
		node.text = String(def['$']['prefix']);
	}
	for(var name in def) {
		name = name.replace(/[^a-z0-9]/gi, '');
		if(name == "fanfic") {
			for(var i = 0;i < def[name].length;++i) {
				var childComp = def[name][i];
				childComp["$"].name = childComp["$"].name.replace(/[^a-z0-9]/gi, '');
				if(!(node[childComp["$"].name] instanceof Object)) node[childComp["$"].name] = new fanfic(childComp["$"].name,node);
				addDefinition(node[childComp["$"].name],childComp);
			}
		}else if(literals.includes(name)) {
			node.literals.push(name);
		}
	}
	return;
}


class rootNodeManager {
	constructor() {
		this.text = "";
		this.nodes = [];
		this.def = {};
		this.badWords = forbiddenDictionary; // MUST BE CENSORED!
		this.error = false;
	}

	rectifier() {
		if(typeof this.text !== "string") {
			throw "What are you trying to do!!!";
		}
		for(var uwu in this.badWords) {
			var bad_word = this.badWords[uwu];
			if(this.text.length < bad_word.length) continue;
			for(var i = 0;i < this.text.length - bad_word.length;++i) {
				var completeMatch = true
				for(var j = 0;j < bad_word.length;++j) {
					if(this.text[i + j] != bad_word[j]) {
						completeMatch = false;
					}
				}
				if(completeMatch) {
					throw "HOW DEAR YOU NOT ORZ ORZ ORZ EYANGCH";
				}
			}
		}
	}

	getNodes() {
		return this.nodes;
	}
}

function generateFanfic(comp) {
	if(comp.prefix) {
		comp.text = comp.prefix;
	}
	for(var i = 0;i < comp.literals.length;++i) {
		comp.text += generateLiteral(comp.literals[i]);
	}
	for(var name in comp) {
		if(comp[name] instanceof fanfic && name != "parent") {
			comp.text += generateFanfic(comp[name]);
		}
	}
	return comp.text;
}

function parseXML(code,callback,root1,root2) {

	var mainRoot = new rootNodeManager();
	xml2js.parseString(code, (err,res) => {
		if(err) {
			mainRoot.error = err;
			callback(mainRoot);
			return;
		}

		try {
			var root = res["root"][root1][0];
			
			if(root["fanfic"]) {
				for(const comp of root["fanfic"]) {
					comp["$"].name = comp["$"].name.replace(/[^a-zA-Z0-9]/gi, '');
					if(mainRoot.def[comp["$"].name] === undefined) {
						mainRoot.def[comp["$"].name] = new fanfic(comp["$"].name,mainRoot);
						addDefinition(mainRoot.def[comp["$"].name],comp);
					}
				}
			}

			var mainRoot_nodes = mainRoot.getNodes();
			for(var name in root) {
				name = name.replace(/[^a-z0-9]/gi, '');
				if(name == "fanfic") continue;
				for(var i = 0;i < root[name].length;++i) {
					if(literals.includes(name)) {
						mainRoot_nodes.push(name);
					}else if(mainRoot.def[name]) {
						var xwx = mainRoot.def[name];
						var currentNode = new fanfic(xwx.name,xwx.parent);
						for(property in xwx) {
							currentNode[property] = xwx[property];
						}

						if(root[name][i]["$"] && root[name][i]["$"].prefix) {
							currentNode.prefix = root[name][i]["$"].prefix;
						}
						mainRoot_nodes.push(currentNode);
					}
				}
			}

			for(const comp of mainRoot_nodes) {
				if(literals.includes(comp)) {
					// it's a literal!
					mainRoot.text += generateLiteral(comp);
				}else if(comp instanceof fanfic) {
					mainRoot.text += generateFanfic(comp);
				}
			}
			mainRoot.rectifier();



			root = res["root"][root2][0];
			var flagRoot = new rootNodeManager();
			if(root["fanfic"]) {
				for(const comp of root["fanfic"]) {
					comp["$"].name = comp["$"].name.replace(/[^a-z0-9]/gi, '');
					if(flagRoot.def[comp["$"].name] === undefined) {
						flagRoot.def[comp["$"].name] = new fanfic(comp["$"].name,flagRoot);
						addDefinition(flagRoot.def[comp["$"].name],comp);
					}
				}
			}

			var flagRoot_nodes = flagRoot.getNodes();
			for(var name in root) {
				name = name.replace(/[^a-z0-9]/gi, '');
				if(name == "fanfic") continue;
				for(var i = 0;i < root[name].length;++i) {
					if(literals.includes(name)) {
						flagRoot_nodes.push(name);
					}else if(flagRoot.def[name]) {
						var xwx = flagRoot.def[name];
						var currentNode = new fanfic(xwx.name,xwx.parent);
						for(property in xwx) {
							currentNode[property] = xwx[property];
						}

						if(root[name][i]["$"] && root[name][i].prefix) {
							currentNode.prefix = root[name][i]["$"].prefix;
						}
						flagRoot_nodes.push(currentNode);
					}
				}
			}

			for(const comp of flagRoot_nodes) {
				if(literals.includes(comp)) {
					// it's a literal!
					flagRoot.text += generateLiteral(comp);
				}else if(comp instanceof fanfic) {
					flagRoot.text += generateFanfic(comp);
				}
			}

			flagRoot.rectifier();
		}catch(err) {
			mainRoot.error = err
		}

		callback(mainRoot);

	});
	return;
}

function viewFanfic(code,res,root1,root2) {
	forbiddenDictionary = {"absolutely not": "eyang bad","no": "eyang only slightly orz","wot!??": "eyang is not my favorite person"};
	parseXML(code,(root) => {
		if(root.error) {
			res.render("viewfanfic", {fanfic: root.error, rick: true});
		}
		res.render("viewfanfic", {fanfic: root.text, rick: false});
	},root1,root2);

}

module.exports = {fanfic, parseXML, viewFanfic};
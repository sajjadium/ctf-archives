const xml2js = require("xml2js");
const canvas = require('canvas')

var literals = ["text", "shape", "line"];

class component {
	constructor(name,parent) {
		this.name = name;
		this.parent = parent;
		this.dx = 0;
		this.dy = 0;
		this.x = 0;
		this.y = 0;
		// <text> <shape> <line> are literals
		this.literals = [];

		if(this == parent) throw "Error: parent cannot be itself!";
	}

	toString() { return this.name; }
}

function addDefinition(node,def) {
	if(def['$']['x']) {
		node.dx = parseInt(def['$']['x']);
	}
	if(def['$']['y']) {
		node.dy = parseInt(def['$']['y']);
	}
	if(def['$']['password']) {
		node.password = def['$']['password'];
	}
	for(var name in def) {
		name = name.replace(/[^a-z0-9]/gi, '');
		if(literals.includes(name)) {
			// it's a literal!
			for(var i = 0;i < def[name].length;++i) {
				node.literals.push(def[name][i]);
				node.literals[node.literals.length - 1].name = name;
				node.literals[node.literals.length - 1].innerText = def[name][i]['_'] ?? '';
			}
		}else if(name == "component") {
			for(var i = 0;i < def[name].length;++i) {
				var childComp = def[name][i];
				childComp["$"].name = childComp["$"].name.replace(/[^a-z0-9]/gi, '');
				if(node[childComp["$"].name] == undefined) node[childComp["$"].name] = new component(childComp["$"].name,node);
				addDefinition(node[childComp["$"].name],childComp);
			}
		}
	}
	return;
}

function drawLiteral(ctx,literal) {
	if(literal['name'] == 'text') {
		ctx.fillStyle = literal['$'].color ?? 'black';
		ctx.font = literal['$'].font ?? "10px bold Arial";
		ctx.fillText(literal.innerText ?? '',parseInt(literal.x),parseInt(literal.y));
	}else if(literal['name'] == 'line') {
		ctx.strokeStyle = literal['$'].color ?? "black";
		ctx.lineWidth = parseInt(literal['$'].width ?? 1);
		ctx.beginPath();
		ctx.moveTo((literal.x ?? 0) + parseInt(literal['$'].x1 ?? 0),(literal.y ?? 0) + parseInt(literal['$'].y1 ?? 0));
		ctx.lineTo((literal.x ?? 0) + parseInt(literal['$'].x2 ?? 0),(literal.y ?? 0) + parseInt(literal['$'].y2 ?? 0));
		ctx.stroke();
	}else if(literal['name'] == 'shape') {
		if(!literal['point'] || literal['point'].length < 3) return;
		ctx.fillStyle = literal['$'].color ?? "black";
		ctx.beginPath();
		ctx.moveTo((literal.x ?? 0) + parseInt(literal['point'][0]['$'].x ?? 0),(literal.y ?? 0) + parseInt(literal['point'][0]['$'].y ?? 0));
		for(var i = 1;i < literal['point'].length;++i) {
			ctx.lineTo((literal.x ?? 0) + parseInt(literal['point'][i]['$'].x ?? 0),(literal.y ?? 0) + parseInt(literal['point'][i]['$'].y ?? 0));
		}
		ctx.closePath();
		ctx.fill();

	}
}

function recurseDraw(ctx,comp) {
	if(comp.parent) {
		comp.x = comp.dx + comp.parent.x;
		comp.y = comp.dy + comp.parent.y;
	}
	for(var i = 0;i < comp.literals.length;++i) {
		comp.literals[i].x = parseInt(comp.literals[i]['$'].x ?? 0) + comp.x;
		comp.literals[i].y = parseInt(comp.literals[i]['$'].y ?? 0) + comp.y;
		drawLiteral(ctx,comp.literals[i]);
	}
	for(var name in comp) {
		if(comp[name] instanceof component && name != "parent") {
			recurseDraw(ctx,comp[name]);
		}
	}
	return;
}

function parseXML(ctx,code,callback) {
	// Store the definitions of all the custom components
	var root = new component("root",null);

	xml2js.parseString(code, (err,res) => {
		if(err) {
			root.error = err;
			callback(root);
			return;
		}

		try {				
			var wrapper = res["fanart"];
			if(wrapper["component"]) {
				for(const comp of wrapper["component"]) {
					comp["$"].name = comp["$"].name.replace(/[^a-z0-9]/gi, '');
					root[comp["$"].name] = new component(comp["$"].name,root);
						addDefinition(root[comp["$"].name],comp);
				}
			}

			for(var name in wrapper) {
				name = name.replace(/[^a-z0-9]/gi, '');
				if(literals.includes(name)) {
					// it's a literal!
					for(const literal of wrapper[name]) {
						literal.name = name;
						if(literal['$'].x) {
							literal.x = parseInt(literal['$'].x);
						}
						if(literal['$'].y) {
							literal.y = parseInt(literal['$'].y);
						}
						if(literal['_']) {
							literal.innerText = literal['_'];
						}
						drawLiteral(ctx,literal);
					}
				}else if(root[name]) {
					for(var i = 0;i < wrapper[name].length;++i) {
						if(wrapper[name][i]["$"].x) {
							root[name].dx = parseInt(wrapper[name][i]["$"].x);
						}
						if(wrapper[name][i]["$"].y) {
							root[name].dy = parseInt(wrapper[name][i]["$"].y);
						}
						if(root[name].password && wrapper[name][i]["$"].password !== root[name].password) {
							continue;
						}
						recurseDraw(ctx,root[name]);
					}
				}
			}
		}catch(err) {
			console.log(err);
			root.error = err
		}

		callback(root);

	});
	return;
}

function getBase64(cvs) {
	return cvs.toBuffer("image/png").toString("base64")
}

function generateArt(code,res) {
	var cvs = canvas.createCanvas(600,600);
	var ctx = cvs.getContext('2d');

	ctx.fillStyle = '#FFF';
	ctx.fillRect(0,0,600,600);

	parseXML(ctx,code,(root) => {
		if(root.error) {
			ctx.fillStyle = '#FFF';
			ctx.fillRect(0,0,600,600);

			ctx.fillStyle = '#000';
			ctx.font = 'bold 10pt Arial';
			ctx.fillText(root.error,100,100);
		}
		res.render("viewart", {img: getBase64(cvs), rick: (root.error != undefined)});
	})

}

module.exports = {component, parseXML, generateArt};
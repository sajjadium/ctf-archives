var allowedProperties = Object.getOwnPropertyNames(Math);

function validateCallExpression(expression) {
	if (expression.type != "CallExpression") {
		throw "Invalid CallExpression";
	}
	if (expression.callee.type != "MemberExpression") {
		throw (
			"Invalid CallExpression, expected type MemberExpression got: " +
			expression.type
		);
	}

	validateMemberExpression(expression.callee);

	if (expression.callee.object.name != "Math") {
		throw (
			"Invalid CallExpression, expected call on object Math, got: " +
			expression.callee.object.name
		);
	}

	for (var argument of expression.arguments) {
		validateCalculation(argument);
	}
}

function validateMemberExpression(expression) {
	if (expression.type != "MemberExpression") {
		throw "Expected type MemberExpression got: " + expression.type;
	}

	validateIdentifier(expression.object);
	validateProperty(expression.property);
}

function validateProperty(property) {
	if (property.type != "Identifier") {
		throw "Invalid property type Identifier got: " + property.type;
	}
	if (!allowedProperties.includes(property.name)) {
		throw "Invalid property " + property.name;
	}
}

function validateCalculation(calculation) {
	if (
		calculation.type == "BinaryExpression" ||
		calculation.type == "LogicalExpression"
	) {
		validateCalculation(calculation.left);
		validateCalculation(calculation.right);
	} else if (calculation.type == "Literal") {
		if (typeof calculation.value != "number") {
			throw "Expected number Literal got: " + typeof calculation.value;
		}
	} else if (calculation.type == "Identifier") {
		validateIdentifier(calculation);
	} else if (calculation.type == "MemberExpression") {
		validateMemberExpression(calculation);
	} else if (calculation.type == "CallExpression") {
		validateCallExpression(calculation);
	} else {
		throw "Invalid calculation type: " + calculation.type;
	}
}

function validateIdentifier(identifier) {
	if (identifier.type != "Identifier") {
		throw "Expected type Identifier found: " + identifier.type;
	}

	if (!/^[a-zA-Z]$/.test(identifier.name) && identifier.name != "Math") {
		throw "Invalid Identifier name: " + identifier.name;
	}
}

function validateExpression(expression) {
	if (expression.type != "AssignmentExpression") {
		throw (
			"Invalid Expression, expected AssignmentExpression got: " +
			expression.type
		);
	}

	validateIdentifier(expression.left);

	validateCalculation(expression.right);
}

function validateProgram(program) {
	for (var statement of program.body) {
		if (statement.type != "ExpressionStatement") {
			throw "Invalid Program";
		}
		validateExpression(statement.expression);
	}
}

document.addEventListener("DOMContentLoaded", () => {
	document.getElementById("btn").onclick = function () {
		runCode(document.getElementById("code").value);
	};

	var params = new URLSearchParams(document.location.search);
	var code = params.get("code");
	if (code) {
		document.getElementById("code").value = code;
		runCode(code);
	}
});

function runCode(code) {
	var params = new URLSearchParams();
	params.set("code", code);
	window.history.replaceState({}, "", "?" + params);
	var AST = esprima.parse(code);
	try {
		validateProgram(AST);
		var html = `Result from evaluating code <code>${code}</code> is ${eval(
			code
		)}`;
		document.getElementById("output").innerHTML = html;
	} catch (e) {
		document.getElementById("output").innerHTML = e;
	}
}

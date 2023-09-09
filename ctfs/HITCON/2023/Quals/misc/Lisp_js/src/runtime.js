const { Tokenizer } = require('./tokenizer')
const { Parser, LispSymbol } = require('./parser')

class LispRuntimeError extends Error {
	constructor(message) {
		super(message)
		this.name = 'LispRuntimeError'
	}
}
exports.LispRuntimeError = LispRuntimeError
class Scope {
	constructor(parent) {
		this.parent = parent
		this.table = Object.create(null)
	}
	get(name) {
		if (Object.prototype.hasOwnProperty.call(this.table, name)) {
			return this.table[name]
		} else if (this.parent) {
			return this.parent.get(name)
		}
	}
	set(name, value) {
		this.table[name] = value
	}
}
exports.Scope = Scope
function astToExpr(ast) {
	if (typeof ast === 'number') {
		return function _numberexpr() {
			return ast
		}
	} else if (typeof ast === 'string') {
		return function _stringexpr() {
			return ast
		}
	} else if (ast instanceof LispSymbol) {
		return function _symbolexpr(scope) {
			// pass null to get the symbol itself
			if (scope === null) return ast
			const r = scope.get(ast.name)
			if (typeof r === 'undefined') throw new LispRuntimeError(`Undefined symbol: ${ast.name}`)
			return r
		}
	} else if (Array.isArray(ast)) {
		return function _sexpr(scope) {
			// pass null to get the ast function call itself
			if (scope === null) return ast
			const fn = astToExpr(ast[0])(scope)
			if (typeof fn !== 'function') throw new LispRuntimeError(`Unable to call a non-function: ${fn}`)
			return fn(ast.slice(1).map(astToExpr), scope)
		}
	} else {
		throw new LispRuntimeError(`Unxpexted ast: ${ast}`)
	}
}
exports.astToExpr = astToExpr
function basicScope() {
	// we always use named function here for a better stack trace
	// otherwise you would see a lot of <anonymous> in the stack trace :(
	const scope = new Scope()
	scope.set('do', function _do(args, scope) {
		const newScope = new Scope(scope)
		let ret = null
		for (const e of args) {
			ret = e(newScope)
			newScope.set('_', ret)
		}
		return ret
	})
	scope.set('print', function _print(args, scope) {
		console.log(...args.map(e => e(scope)))
	})
	scope.set('+', function _plus(args, scope) {
		return args[0](scope) + args[1](scope)
	})
	scope.set('-', function _minus(args, scope) {
		return args.length === 1 ? -args[0](scope) : args[0](scope) - args[1](scope)
	})
	scope.set('*', function _multiply(args, scope) {
		return args[0](scope) * args[1](scope)
	})
	scope.set('/', function _divide(args, scope) {
		return args[0](scope) / args[1](scope)
	})
	scope.set('<', function _lessThan(args, scope) {
		return args[0](scope) < args[1](scope)
	})
	scope.set('>', function _greaterThan(args, scope) {
		return args[0](scope) > args[1](scope)
	})
	scope.set('<=', function _lessThanOrEqual(args, scope) {
		return args[0](scope) <= args[1](scope)
	})
	scope.set('>=', function _greaterThanOrEqual(args, scope) {
		return args[0](scope) >= args[1](scope)
	})
	scope.set('=', function _equal(args, scope) {
		return args[0](scope) === args[1](scope)
	})
	scope.set('.', function _dot(name, scope) {
		const obj = name[0](scope)
		const prop = name[1](scope)
		const ret = obj[prop]
		if (typeof ret === 'undefined') {
			throw new LispRuntimeError(`Undefined property: ${prop}`)
		}
		return ret
	})
	scope.set('if', function _if(args, scope) {
		if (args.length !== 3) throw new LispRuntimeError('if expects 3 arguments')
		const cond = args[0](scope)
		if (cond) return args[1](scope)
		else return args[2](scope)
	})
	scope.set('let', function _let(args, scope) {
		if (args.length !== 2) throw new LispRuntimeError('let expects 2 arguments')
		const varSym = args[0](null)
		if (!(varSym instanceof LispSymbol)) throw new LispRuntimeError('let expects a symbol as first argument')
		const value = args[1](scope)
		scope.set(varSym.name, value)
	})
	scope.set('fun', function _fun(args, definingScope) {
		if (args.length !== 2) throw new LispRuntimeError('fun expects 2 arguments')
		const argSyms = args[0](null)
		if (!Array.isArray(argSyms)) throw new LispRuntimeError('fun expects a list of symbols as first argument')
		if (!argSyms.every(e => e instanceof LispSymbol))
			throw new LispRuntimeError('fun expects a list of symbols as first argument')
		const body = args[1]
		return function _runtimeDefinedFunction(fnargs, callerScope) {
			if (fnargs.length !== argSyms.length)
				throw new LispRuntimeError(`Function expects ${argSyms.length} arguments, got ${fnargs.length}`)
			// const fnScope = new Scope(callerScope)  // dynamic scope
			const fnScope = new Scope(definingScope) // lexical scope
			for (let i = 0; i < argSyms.length; i++) {
				fnScope.set(argSyms[i].name, fnargs[i](callerScope))
			}
			return body(fnScope)
		}
	})
	scope.set('list', function _list(args, scope) {
		return args.map(e => e(scope))
	})
	scope.set('slice', function _slice(args, scope) {
		if (args.length !== 3) throw new LispRuntimeError('slice expects 3 arguments')
		const list = args[0](scope)
		const start = args[1](scope)
		const end = args[2](scope)
		if (!Array.isArray(list)) throw new LispRuntimeError('slice expects a list as first argument')
		return list.slice(start, end)
	})
	scope.set('object', function _object(args, scope) {
		return Object.fromEntries(args.map(e => e(scope)))
	})
	scope.set('keys', function _keys(args, scope) {
		const obj = args[0](scope)
		return Object.keys(obj)
	})
	return scope
}
exports.basicScope = basicScope
function extendedScope() {
	// a runtime with all the basic functions, plus some more js interop functions
	const scope = basicScope()
	scope.set('Object', Object)
	scope.set('Array', Array)
	scope.set('String', String)
	scope.set('Number', Number)
	scope.set('Boolean', Boolean)
	scope.set('Date', Date)
	scope.set('Math', Math)
	scope.set('JSON', JSON)
	scope.set('j2l', function _j2l(args, scope) {
		if (args.length !== 1) throw new LispRuntimeError('j2l expects 1 argument')
		const fn = args[0](scope)
		if (typeof fn !== 'function') throw new LispRuntimeError('j2l expects a function as argument')
		return function _wrapperForJSFunction(fnargs, callerScope) {
			return fn(...fnargs.map(e => e(callerScope)))
		}
	})
	scope.set('l2j', function _l2j(args, scope) {
		if (args.length !== 1) throw new LispRuntimeError('l2j expects 1 argument')
		const fn = args[0](scope)
		if (typeof fn !== 'function') throw new LispRuntimeError('l2j expects a function as argument')
		return function _wrapperForLispFunction(...args) {
			return fn(
				args.map(x => () => x),
				scope
			)
		}
	})
	scope.set('..', function _dot(args, scope) {
		const obj = args[0](scope)
		const prop = args[1](scope)
		let ret = obj[prop]
		if (typeof ret === 'undefined') {
			throw new LispRuntimeError(`Undefined property: ${prop}`)
		}
		if (typeof ret !== 'function') {
			throw new LispRuntimeError(`Property ${prop} is not a function`)
		}
		return Function.prototype.bind.call(ret, obj)
	})
	return scope
}
exports.extendedScope = extendedScope
function lispEval(code, scope = basicScope()) {
	const tokens = Tokenizer.tokenize(code)
	const ast = Parser.parse(tokens)
	return astToExpr(ast)(scope)
}
exports.lispEval = lispEval

if (require.main === module) {
	// this serves as a test suite :)
	// and a guide on how to use this lisp dialect
	lispEval(`
(do 
	(let x 5)
	(let add (fun (x y) (+ x y)))
	(print (- 1 x))
	(print (add 2 3))
	(print (if (< x 0) "x is negative" "x is positive"))
	(let fib (fun (n) (if (< n 2) 1 (+ (fib (- n 1)) (fib (- n 2))))))
	(print fib)
	(print (= (fib 10) 89))
	(print ((fun (x) (+ x 1)) 1))
	(print (((fun (x) (fun (y) (+ x y))) "hello") " world"))

	(let val 1234)
	(let checkval (fun () (print (if (= val 1234) "lexical scope" "dynamic scope"))))
	(do
		(let val 5678)
		(checkval)
	)
	(print (if (= val 1234) "val does not escape" "val escapes"))

	0
	(+ _ 1)
	(+ _ 2)
	(+ _ 3)
	(+ _ 4)
	(print (if (= _ 10) "yeah _ actually works" ":("))
	
	(print (list 1 2 "x" val (fib 5)))
	(let obj (object
		(list "a" 1)
		(list "b" 2)
		(list "c" 3)
	))
	(print obj)
	(print (. (list 1 2 3) "length"))
	(print (keys obj))
	(let sum (fun (arr acc) (do
		(let len (. arr "length"))
		(let rest (slice arr 1 len))
		(if (= len 0) acc (sum rest (+ acc (. arr "0"))))
	)))
	(print (sum (list 1 2 3 4 5 6 7 8 9 10) 0))
	(print (sum (keys obj) ""))
)
`)
	console.log('----------')
	const add1 = lispEval(
		`
(do
	(let x 5)
	(let isArray (j2l (. Array "isArray")))
	(print (isArray x))
	(print (isArray (list)))

	(let arr (list 1 2 3))
	(let mapfn (fun (x _ _) (+ x 1)))
	(print ((j2l (.. arr "map")) (l2j mapfn)))
	(print "Date.now() =" ((j2l (. Date "now"))))
	(l2j (fun (x) (+ x 1)))
)
`,
		extendedScope()
	)
	console.log(add1(1))
}

class ParserError extends Error {
	constructor(message) {
		super(message)
		this.name = 'ParserError'
	}
}
exports.ParserError = ParserError
class LispSymbol {
	constructor(name) {
		this.name = name
	}
}
exports.LispSymbol = LispSymbol
class Parser {
	constructor(tokens) {
		this.tokens = tokens
		this.idx = 0
	}
	peek() {
		if (this.idx >= this.tokens.length) return null
		return this.tokens[this.idx]
	}
	next() {
		if (this.idx >= this.tokens.length) throw new ParserError('Unexpected end of input')
		return this.tokens[this.idx++]
	}
	number() {
		const token = this.next()
		if (token.type !== 'number') throw new ParserError('Expected number')
		return parseInt(token.value)
	}
	string() {
		const token = this.next()
		if (token.type !== 'string') throw new ParserError('Expected string')
		return token.value
	}
	symbol() {
		const token = this.next()
		if (token.type !== 'symbol') throw new ParserError('Expected symbol')
		return new LispSymbol(token.value)
	}
	sexp() {
		const token = this.next()
		if (token.type !== 'lparen') throw new ParserError('Expected (')
		let sexp = []
		while (this.peek()?.type !== 'rparen') {
			sexp.push(this.expr())
		}
		this.next()
		return sexp
	}
	expr() {
		const token = this.peek()
		if (token === null || token.type === 'eof') throw new ParserError('Unexpected end of input')
		else if (token.type === 'number') return this.number()
		else if (token.type === 'string') return this.string()
		else if (token.type === 'symbol') return this.symbol()
		else if (token.type === 'lparen') return this.sexp()
		else throw new ParserError(`Unexpected token: type=${token.type} value=${token.value}`)
	}
	static parse(tokens) {
		const parser = new Parser(tokens)
		const ret = parser.expr()
		const next = parser.peek()
		if (next?.type !== 'eof')
			throw new ParserError(`Expected end of input, but got more tokens: type=${next?.type} value=${next?.value}`)
		return ret
	}
}
exports.Parser = Parser

class TokenizerError extends Error {
	constructor(message) {
		super(message)
		this.name = 'TokenizerError'
	}
}
exports.TokenizerError = TokenizerError
class Tokenizer {
	constructor(code) {
		this.code = code
		this.idx = 0
	}
	peek() {
		if (this.idx >= this.code.length) return null
		return this.code[this.idx]
	}
	next() {
		if (this.idx >= this.code.length) throw new TokenizerError('Unexpected end of input')
		return this.code[this.idx++]
	}
	isSpace(c) {
		return c === ' ' || c === '\t' || c === '\n'
	}
	isDigit(c) {
		const cc = c.charCodeAt(0)
		return cc >= '0'.charCodeAt(0) && cc <= '9'.charCodeAt(0)
	}
	isAlpha(c) {
		const cc = c.charCodeAt(0)
		return (
			(cc >= 'a'.charCodeAt(0) && cc <= 'z'.charCodeAt(0)) || (cc >= 'A'.charCodeAt(0) && cc <= 'Z'.charCodeAt(0))
		)
	}
	isQuote(c) {
		return c == '"'
	}
	isSymbolStart(c) {
		return this.isSymbol(c) && !this.isDigit(c)
	}
	isSymbol(c) {
		return (
			this.isAlpha(c) ||
			this.isDigit(c) ||
			c == '+' ||
			c == '-' ||
			c == '*' ||
			c == '/' ||
			c == '<' ||
			c == '>' ||
			c == '=' ||
			c == '_' ||
			c == '.'
		)
	}
	isLParen(c) {
		return c == '('
	}
	isRParen(c) {
		return c == ')'
	}
	scanNumber() {
		let num = ''
		while (this.isDigit(this.peek())) {
			num += this.next()
		}
		return { type: 'number', value: num }
	}
	scanString() {
		let str = ''
		if (!this.isQuote(this.next())) throw new TokenizerError('String must start with "')
		while (!this.isQuote(this.peek())) {
			str += this.next()
		}
		if (!this.isQuote(this.next())) throw new TokenizerError('String must end with "')
		return { type: 'string', value: str }
	}
	scanSymbol() {
		let sym = ''
		if (!this.isSymbolStart(this.peek())) throw new TokenizerError('Symbol must start with a letter')
		while (this.isSymbol(this.peek())) {
			sym += this.next()
		}
		return { type: 'symbol', value: sym }
	}
	skipSpace() {
		while (this.isSpace(this.peek())) {
			this.next()
		}
	}
	scan() {
		const c = this.peek()
		if (c === null) {
			return { type: 'eof', value: null }
		} else if (this.isDigit(c)) {
			return this.scanNumber()
		} else if (this.isQuote(c)) {
			return this.scanString()
		} else if (this.isSymbolStart(c)) {
			return this.scanSymbol()
		} else if (this.isLParen(c)) {
			return { type: 'lparen', value: this.next() }
		} else if (this.isRParen(c)) {
			return { type: 'rparen', value: this.next() }
		} else {
			throw new TokenizerError('Unexpected token')
		}
	}
	scanAll() {
		let tokens = []
		while (this.idx < this.code.length) {
			this.skipSpace()
			tokens.push(this.scan())
		}
		return tokens
	}
	static tokenize(code) {
		return new Tokenizer(code).scanAll()
	}
}
exports.Tokenizer = Tokenizer

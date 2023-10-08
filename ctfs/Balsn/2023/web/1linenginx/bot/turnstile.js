const xf = require('xfetch-js')

const SECRET_KEY = process.env.TURNSTILE_SECRET_KEY
if (!SECRET_KEY) {
	console.info('Turnstile verification is disabled due to the lack of TURNSTILE_SECRET_KEY')
}
module.exports = async (req, res, next) => {
	if (!SECRET_KEY) return next()
	const captcha = req.body?.['cf-turnstile-response']
	if (!captcha) {
		return res.status(400).send('No captcha token found')
	}
	const resp = await xf
		.post('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
			formData: {
				secret: SECRET_KEY,
				response: captcha
			}
		})
		.json()
	if (resp.success) {
		return next()
	} else {
		return res.status(400).send('Captcha verification failed')
	}
}

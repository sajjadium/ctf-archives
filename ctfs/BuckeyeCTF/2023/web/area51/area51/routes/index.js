import { Router } from 'express';
const router = Router();
import User from '../User.js';

router.get('/', (req, res) => {
	var session = res.cookies.get("session");
	if (session) {
		session = JSON.parse(session);

		var token = session.token
		return User.find({
			session: token
		}).then((user) => {
			if (user.length == 1) {
				return res.render('dashboard');
			}

			return res.render('index');
		})
		.catch((e) => {
			res.json({ message: 'Hm server errored'});
		});
	}
	return res.render('index');
});

router.post('/api/login', (req, res) => {
	let { username, password } = req.body;

	if (username && password && typeof username === 'string' && typeof password === 'string') {

		return User.find({ 
			username,
			password,
			admin: false
		})
			.then((user) => {
				if (user.length == 1) {
					var new_session = {
						token: user[0].session,
						username: user[0].username
					}
					res.cookies.set("session", JSON.stringify(new_session));

					if (user[0].admin) {
						return res.json({logged: 1, message: `Success! Welcome back chief stormer.` });
					} else {
						return res.json({logged: 1, message: `Success, welcome back ${user[0].username}.` });
					}
				} else {
					return res.json({logged: 0, message: 'Login failed :/'});
				}
			})
			.catch((e) => {
				return res.json({ message: 'Hm server errored'});
			});
	}
	return res.json({ message: 'Login failed :/'});
});

export default router;
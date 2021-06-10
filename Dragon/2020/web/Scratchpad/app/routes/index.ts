import * as express from 'express';
import utils from '../utils';


const router = express.Router();

router.get('/', (_req, res) => res.render('index'));
router.get(
    '/logout', (req, res) => utils.signOut(req, () => res.redirect('/')));
router.get('/login', (_req, res) => res.render('login', {title: 'Log in'}));
router.post('/login', async (req, res) => {
  const user = await res.locals.db.users.findOne({name: req.body.name});
  if (!user || !utils.checkPassword(user, req.body.password)) {
    return res.render(
        'login', {title: 'Log in', error: 'Invalid username or password'});
  }

  utils.signIn(req, user);
  res.redirect('/notes');
});

router.get(
    '/register', (_req, res) => res.render('register', {title: 'Register'}));
router.post('/register', async (req, res) => {
  const regexp = /^\s*$/;
  let errors = [];

  if (regexp.test(req.body.name)) {
    errors.push(`Username can't be empty.`);
  }

  if (regexp.test(req.body.password)) {
    errors.push(`Password can't be empty.`);
  }

  if (req.body.password !== req.body.password_confirmation) {
    errors.push(`Password doesn't match the confirmation.`);
  }

  if (errors.length !== 0) {
    return res.render('register', {title: 'Register', error: errors.join(' ')});
  }

  try {
    await res.locals.db.users.insert(
        {name: req.body.name, password: utils.hashPassword(req.body.password)});
  } catch (err) {
    return res.render(
        'register', {title: 'Register', error: 'User already exists'});
  }

  return res.redirect('/login');
});

export default router;

import * as express from 'express';
import * as createError from 'http-errors';

const router = express.Router();

router.get('/', async (req, res, next) => {
  if (req.query.q) {
    try {
      const notes = await res.locals.db.notes.find({
        user_id: req.session.userId,
        or: [{'title ~': req.query.q}, {'content ~': req.query.q}]
      });

      if (notes.length == 0) {
        return next(createError(404));
      }

      return res.render('notes', {notes});
    } catch (e) {
      return next(createError(500));
    }
  }

  const notes = await res.locals.db.notes.find({user_id: req.session.userId});
  return res.render('notes', {notes});
});

router.get('/new', (_req, res) => res.render('new'));
router.post('/new', async (req, res) => {
  let errors = [];
  const regex = /^\s*$/;

  if (regex.test(req.body.title)) {
    errors.push('Title is blank.');
  }

  if (regex.test(req.body.content)) {
    errors.push('Content is blank.');
  }

  if (errors.length !== 0) {
    return res.render('new', {error: errors.join(' ')});
  }

  try {
    const result = await res.locals.db.notes.save({
      user_id: req.session.userId,
      title: req.body.title,
      content: req.body.content,
      favourite: req.body.favourite
    });
    return res.redirect(`/notes/${result.id}`);
  } catch (err) {
    return res.render('new', {error: 'Error adding a note'});
  }
});

router.get('/:id/edit', async (req, res, next) => {
  const note = await res.locals.db.notes.findOne(
      {user_id: req.session.userId, id: req.params.id});
  if (!note) {
    return next(createError(404));
  }
  res.render('edit', {note});
});
router.post('/:id/edit', async (req, res) => {
  let errors = [];
  const regex = /^\s*$/;

  if (regex.test(req.body.title)) {
    errors.push('Title is blank.');
  }

  if (regex.test(req.body.content)) {
    errors.push('Content is blank.');
  }

  if (errors.length !== 0) {
    return res.render('edit', {
      error: errors.join(' '),
      note: {
        id: req.params.id,
        title: req.body.title,
        content: req.body.content,
        favourite: req.body.favourite
      }
    });
  }

  try {
    await res.locals.db.notes.update(
        {
          id: req.params.id,
          user_id: req.session.userId,
        },
        {
          title: req.body.title,
          content: req.body.content,
          favourite: req.body.favourite
        });
    return res.redirect(`/notes/${req.params.id}`);
  } catch (err) {
    return res.render('edit', {
      error: 'Error editing a note',
      note: {
        id: req.params.id,
        title: req.body.title,
        content: req.body.content,
        favourite: req.body.favourite
      }
    });
  }
});


router.post('/:id/delete', async (req, res) => {
  try {
    await res.locals.db.notes.destroy(
        {user_id: req.session.userId, id: req.params.id});
  } catch (err) {
    return res.render('index', {error: 'An error occurred'});
  }

  res.redirect('/notes');
});


router.post('/:id/report', async (req, res) => {
  try {
    await res.locals.db.reports.insert({id: req.params.id});
  } catch (err) {
    return res.render('index', {error: 'Already reported'});
  }

  return res.render('index', {notice: 'Request successfully submitted'});
});


router.get('/:id', async (req, res, next) => {
  try {
    const note = await res.locals.db.notes.findOne({id: req.params.id});
    res.render('note', {note});
  } catch (err) {
    next(createError(404));
  }
});

export default router;

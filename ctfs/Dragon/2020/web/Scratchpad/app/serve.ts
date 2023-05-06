import * as assert from 'assert';
import * as bodyParser from 'body-parser';
import * as csrf from 'csurf';
import * as express from 'express';
import {NextFunction, Request, Response} from 'express';
import * as session from 'express-session';
import * as createError from 'http-errors';
import {HttpError} from 'http-errors';
import * as massive from 'massive';
import * as logger from 'morgan';
import * as path from 'path';

import indexRouter from './routes/index';
import notesRouter from './routes/notes';
import utils from './utils';

async function main() {
  process.on('unhandledRejection', (reason, _) => {
    console.log(reason);
  });

  assert.ok(process.env.DB, 'DB is not set');
  assert.ok(process.env.SESSION_SECRET, 'SESSION_SECRET is not set');

  const db = await massive(process.env.DB);
  const app = express();
  app.set('views', path.join(__dirname, 'views'));
  app.set('view engine', 'pug');

  app.use(logger('dev'));
  app.use('/static', express.static(path.join(__dirname, 'static')));

  app.use(session({
    secret: process.env.SESSION_SECRET,
    saveUninitialized: true,
    resave: false,
    store: new (require('memorystore')(session))(
        {checkPeriod: 7200000, max: 0x32000000})
  }));
  app.use(bodyParser.urlencoded({extended: false}));
  app.use(csrf({}));

  app.use((req: Request, res: Response, next: NextFunction) => {
    res.locals.db = db;
    res.locals.query = req.query.q;
    res.locals.session = req.session;
    res.locals.csrfToken = req.csrfToken();

    res.set('Content-Security-Policy', `
      default-src 'none';
      style-src 'self';
      img-src 'self';
      form-action 'self';
      base-uri 'none';
    `.replace(/\n/g, ''));

    next();
  });

  app.use('/', indexRouter);
  app.use('/notes', utils.checkAuth, notesRouter);

  app.use((_req: Request, _res: Response, next: NextFunction) => {
    next(createError(404));
  });

  app.use(
      (err: HttpError, _req: Request, res: Response, next: NextFunction) => {
        if (res.headersSent) {
          return next(err);
        }

        res.locals.message = err.message;
        res.locals.status = err.status;
        res.status(err.status || 500);
        res.render(
            'error',
        );
      });
  app.listen(3000);
};

main();

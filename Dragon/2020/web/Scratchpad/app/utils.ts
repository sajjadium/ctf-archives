import { hashSync, compareSync, genSaltSync } from 'bcrypt';
import { Request, Response, NextFunction } from 'express';

export default class Utils {
  static hashPassword(password: string): string {
    return hashSync(password, genSaltSync());
  }

  static checkPassword(user: any, password: string): boolean {
    return compareSync(password, user.password);
  }

  static signIn(req: Request, user: any) {
    req.session.userId = user.id;
  }

  static signOut(req: Request, next: NextFunction) {
    req.session.destroy(next);
  }

  static checkAuth(req: Request, res: Response, next: NextFunction): any {
    if (!req.session.userId) {
      return res.redirect('/login');
    }
    next();
  }
}



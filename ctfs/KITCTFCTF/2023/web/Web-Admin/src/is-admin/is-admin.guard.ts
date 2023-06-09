import { CanActivate, ExecutionContext, Injectable } from '@nestjs/common';
import { Observable } from 'rxjs';

@Injectable()
export class IsAdminGuard implements CanActivate {
  canActivate(
    context: ExecutionContext,
  ): boolean | Promise<boolean> | Observable<boolean> {
    const { user } = context.switchToHttp().getRequest();
    const adminUser: { isAdmin?: boolean } = {};
    if (user?.isAdmin) {
      adminUser.isAdmin = true;
    }
    if (adminUser.isAdmin) {
      return true;
    }
    return false;
  }
}

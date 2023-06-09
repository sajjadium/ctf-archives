import { Controller, Get, Post, Body, Query } from '@nestjs/common';
import { UserService } from './user.service';
import { User } from './user.entity';

interface UserDto {
  username: string;
  password: string;
}

@Controller('user')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post('/signup')
  createUser(@Body() body: UserDto): Promise<User | null> {
    const username = body?.username;
    const password = body?.password;

    return this.userService.create({ username, password });
  }

  @Get('/login')
  async login(
    @Query('username') username: string,
    @Query('password') password: string,
  ): Promise<{ success: boolean; auth_token?: string | null }> {
    if (!username || !password) return { success: false };

    const user = await this.userService.findOne(username);
    if (!user) return { success: false };

    if (await this.userService.isCorrectPassword(password, user.passwordHash)) {
      const token = this.userService.generateJwt(user);
      return { success: true, auth_token: `Bearer ${token}` };
    }

    return { success: false };
  }
}

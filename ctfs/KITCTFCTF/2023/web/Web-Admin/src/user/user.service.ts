import { Injectable, OnModuleInit } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from './user.entity';
import { hash } from 'bcrypt';
import { compare } from 'bcrypt';
import { JwtService } from '@nestjs/jwt';
import { ConfigService } from '@nestjs/config';

const SALT_OR_ROUNDS = 10;
const ADMIN_USERNAME = 'admin';

interface JwtPayload {
  id: number;
  username: string;
  isAdmin: boolean;
}

@Injectable()
export class UserService implements OnModuleInit {
  constructor(
    @InjectRepository(User)
    private usersRepository: Repository<User>,
    private jwtService: JwtService,
    private configService: ConfigService,
  ) {}

  async onModuleInit() {
    const adminExists = await this.usersRepository.findOneBy({
      username: ADMIN_USERNAME,
    });

    if (!adminExists) {
      const admin = new User();
      admin.username = ADMIN_USERNAME;
      admin.passwordHash = await this.generateHashedPassword(
        this.configService.get<string>('ADMIN_PASSWORD') || 'demoPass',
      );
      admin.isAdmin = true;
      await this.usersRepository.save(admin);
    }
  }

  findOne(username: string): Promise<User | null> {
    return this.usersRepository.findOne({
      where: { username, passwordHash: undefined, isAdmin: undefined },
    });
  }

  generateHashedPassword = async (password: string) => {
    const passwordHash = await hash(password, SALT_OR_ROUNDS);
    return passwordHash;
  };

  isCorrectPassword = async (password: string, passwordHash: string) => {
    return compare(password, passwordHash);
  };

  async create(dto: {
    username: string;
    password: string;
  }): Promise<User | null> {
    const userExists = await this.usersRepository.findOneBy({
      username: dto.username,
    });
    if (userExists) {
      return null;
    }
    const user = new User();
    user.username = dto.username;
    user.passwordHash = await this.generateHashedPassword(dto.password);
    user.isAdmin = false;
    await this.usersRepository.save(user);
    user.passwordHash = '*redacted*';
    return user;
  }

  generateJwt(user: JwtPayload) {
    const payload = { ...user, passwordHash: null };
    return this.jwtService.sign(payload);
  }

  validateJwt(token: string) {
    return this.jwtService.verify(token);
  }
}

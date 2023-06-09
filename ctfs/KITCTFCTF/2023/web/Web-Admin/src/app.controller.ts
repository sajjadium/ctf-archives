import { Controller, Get, Query, UseGuards } from '@nestjs/common';
import { AppService } from './app.service';
import { IsAdminGuard } from './is-admin/is-admin.guard';
import { AuthGuard } from './auth/auth.guard';
import { ConfigService } from '@nestjs/config';

@Controller()
export class AppController {
  constructor(
    private readonly appService: AppService,
    private configService: ConfigService,
  ) {}

  @Get('/enableAttribute')
  enableAttribute(
    @Query('attribute') attribute: string,
    @Query('value') value: string,
  ): boolean {
    return this.appService.enableAttribute(attribute, value);
  }

  @Get('/disableAttribute')
  disableAttribute(
    @Query('attribute') attribute: string,
    @Query('value') value: string,
  ): boolean {
    return this.appService.disableAttribute(attribute, value);
  }

  @Get('/enabledAttributes')
  enabledAttributes(): any {
    return this.appService.getEnabledAttributeValues();
  }

  @Get('/flag')
  @UseGuards(AuthGuard, IsAdminGuard)
  getFlag(): string {
    return this.configService.get<string>('FLAG') || 'flag{d3m0Fl4g}';
  }
}

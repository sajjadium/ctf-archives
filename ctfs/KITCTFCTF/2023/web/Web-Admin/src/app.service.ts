import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  enabledAttributeValues: any;
  constructor() {
    this.enabledAttributeValues = {};
  }

  enableAttribute(attribute: string, value: string): boolean {
    if (!this.enabledAttributeValues[attribute]) {
      this.enabledAttributeValues[attribute] = {};
    }
    this.enabledAttributeValues[attribute][value] = true;

    return true;
  }

  disableAttribute(attribute: string, value: string): boolean {
    if (!this.enabledAttributeValues[attribute]) {
      this.enabledAttributeValues[attribute] = {};
    }
    this.enabledAttributeValues[attribute][value] = false;

    return true;
  }

  getEnabledAttributeValues(): any {
    return this.enabledAttributeValues;
  }
}

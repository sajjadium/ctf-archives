// This file is created by egg-ts-helper@1.34.7
// Do not modify this file!!!!!!!!!
/* eslint-disable */

import 'egg';
import ExportHome = require('../../../app/controller/home');

declare module 'egg' {
  interface IController {
    home: ExportHome;
  }
}

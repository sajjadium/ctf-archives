'use strict';
const { curly } = require('node-libcurl');
const fs = require('fs');
const md5 = require('md5');
const { Controller } = require('egg');

class HomeController extends Controller {
  async snapshot() {
    const { ctx, app } = this;
    // curl and snapshot and log
    if (typeof ctx.query.url !== 'string' || ctx.query.url === '') {
      ctx.body = 'invalid url';
      return;
    }
    try {
      const { headers, data } = await curly.get(ctx.query.url);
      const userPath = '/tmp/snapshots/' + md5(ctx.ip);
      if (!fs.existsSync(userPath)) {
        fs.mkdirSync(userPath);
      }
      fs.writeFileSync(userPath + '/' + md5(ctx.query.url), data);
      ctx.body = headers;
      const _ctx = {
        request: {
          ip: ctx.request.ip,
          path: ctx.request.path,
          method: ctx.request.method,
          headers: ctx.request.headers,
        },
      };
      app.emit('snapshot_start', _ctx, headers);
    } catch (e) {
      console.log(e);
      ctx.body = 'error';
    }
  }
  async query() {
    const { ctx } = this;
    const result = await this.app.auditLog.model.find({ ip: ctx.ip });
    ctx.body = result;
  }

  async index() {
    const { ctx } = this;
    ctx.body = 'hello egg.js';
  }
}

module.exports = HomeController;

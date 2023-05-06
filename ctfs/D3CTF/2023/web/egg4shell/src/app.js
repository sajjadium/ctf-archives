// app.js
const fs = require('fs');

class AppBootHook {
  constructor(app) {
    this.app = app;
  }
  async didReady() {
    // 应用已经启动完毕
    this.app.snapshotLogTree = {};
    if (!fs.existsSync('/tmp/snapshots')) {
      fs.mkdirSync('/tmp/snapshots');
    }
    this.app.watcher.watch('/tmp/snapshots/', r => {
      const path = r.path.split('/').slice(1);
      path.reduce((a, c, counter) => {
        if (counter === path.length - 1) {
          a[c] = r.event;
        } else if (!a[c] || typeof a[c] !== 'object') a[c] = {};
        return a[c];
      }, this.app.snapshotLogTree);
      process.nextTick(() => {
        if (this.ctx && this.headers) { this.app.emit('snapshot_end', this.ctx, this.headers); }
      });
    });
    this.app.on('snapshot_start', (ctx, headers) => {
      this.ctx = ctx;
      this.headers = headers;
    });
    this.app.on('snapshot_end', (ctx, headers) => {
      this.app.auditLog.log(ctx, {
        operationType: 'snapshot',
        operationContent: 'headers',
        body: { headers, snapshotLog: this.app.snapshotLogTree },
      });
    });
  }
}

module.exports = AppBootHook;

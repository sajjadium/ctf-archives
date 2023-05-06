'use strict';

/** @type Egg.EggPlugin */
module.exports = {
  // had enabled by egg
  // static: {
  //   enable: true,
  // }
  auditLog: {
    enable: true,
    package: 'egg-audit-log',
  },
};

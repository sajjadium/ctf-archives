/* eslint valid-jsdoc: "off" */

'use strict';

/**
 * @param {Egg.EggAppInfo} appInfo app info
 */
module.exports = appInfo => {
  /**
   * built-in config
   * @type {Egg.EggAppConfig}
   **/
  const config = exports = {};

  // use for cookie sign key, should change to your own and keep security
  config.keys = appInfo.name + '_1677738387159_5544';

  // add your middleware config here
  config.middleware = [];

  // add your user config here
  const userConfig = {
    // myAppName: 'egg',
  };
  config.watcher = {
    type: 'development', // default event source
  };
  config.auditLog = {
    model: {
      name: 'audit_log',
      expand: { body: '' },
    },
    mongoose: {
      url: 'mongodb://mongo/egg4shell',
      options: {
        auth: {authSource: "admin"},
        user: 'admin',
        pass: '********' // omit
      },
    },
  };

  return {
    ...config,
    ...userConfig,
  };
};

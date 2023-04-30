'use strict';
/**
 * @param {Egg.Application} app - egg application
 */
module.exports = app => {
  const { router, controller } = app;
  router.get('/snapshot', controller.home.snapshot);
  router.get('/query', controller.home.query);
  // eslint-disable-next-line no-unused-vars
  router.get('/', controller.home.index);
};

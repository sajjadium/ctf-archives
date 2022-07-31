/* global __dirname: false */

const path = require('path');

module.exports = {
  mode: 'development',
  devtool: 'hidden-cheap-source-map',
  entry: './webpack-index.js',
  output: {
    filename: 'nodejs-bundled.js',
    path: path.resolve(__dirname, 'dist'),
  },
  resolve: {
    modules: [path.resolve(__dirname, 'overrides'), path.resolve(__dirname, 'nodejs')],
    fallback: {
      path: false,
      util: false,
      vm: false,
      'internal/bootstrap/loaders': false,
      'internal/crypto/keys': false,
      'internal/tty': false,
      'internal/url': false,
    },
  },
};

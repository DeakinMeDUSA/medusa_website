const {
  addDecoratorsLegacy,
  override,
  disableEsLint,
  addWebpackPlugin,
} = require('customize-cra')
const { deletePlugin } = require('customize-cra-plugin')
const _ = require('underscore')
const apps = require('./src/index').apps
var BundleTracker = require('webpack-bundle-tracker')

const setChunksName = name => config => {
  config.optimization.splitChunks.name = name
  config.optimization.splitChunks.minChunks = 2
  return config
}

const setConfigEntry = b => config => {
  config.entry = _.mapObject(apps, appSubmodulePath => [
    require.resolve(`./src/${appSubmodulePath}`),
  ])
  return config
}

module.exports = {
  webpack: override(
    deletePlugin('ManifestPlugin'),
    setConfigEntry(),
    addDecoratorsLegacy(),
    disableEsLint(),
    addWebpackPlugin(new BundleTracker({
      path: __dirname,
      filename: './build/webpack-stats.json',
      logTime: true,
    })),
    setChunksName('vendors'),
  ),
}

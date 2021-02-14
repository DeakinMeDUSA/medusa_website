const {
  addDecoratorsLegacy,
  override,
  disableEsLint,
  addWebpackPlugin,
  setWebpackOptimizationSplitChunks,
} = require('customize-cra')

var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  webpack: override(
    addDecoratorsLegacy(),
    disableEsLint(),
    addWebpackPlugin(new BundleTracker({
      path: __dirname,
      filename: './build/webpack-stats.json',
      logTime: true,
    })),
    setWebpackOptimizationSplitChunks({
        // chunks: "all",
        name: "vendor"
      },
    ),
  )
}

// setChunksName('vendors')

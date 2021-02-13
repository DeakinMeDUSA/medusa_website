const path = require('path')
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
  mode: 'development',  // or 'production'
  entry: './src/index.tsx',  // path to our input file
  output: {
    filename: 'index-bundle.js',  // output bundle file name
    path: path.resolve(__dirname, './build/static'),  // path to our Django static directory
  },
  resolve: {
    extensions: ['.js', '.jsx', '.tsx', '.ts'],
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.jsx|\.js/,
        use: {
          loader: 'babel-loader',
          options: { presets: ['@babel/preset-react', '@babel/preset-env'] },
        },
        exclude: /node_modules/,
      },
      {
        test: /\.scss/,
        use: ['style-loader', 'css-loader', 'postcss-lodaer', 'sass-loader'], // Note that postcss loader must come before sass-loader
      },
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      },
      {
          test: /\.(jpe?g|png|gif|svg)$/i,
          loader: 'file-loader',
          options: {
            name: '[path][name].[ext]',
          }
      }
    ],
  },
}

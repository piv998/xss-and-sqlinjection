const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const pages = [
  'index',
  'add_flag',
  'get_flag',
];

const htmls = pages.map(x => new HtmlWebpackPlugin({
  chunks: [x],
  filename: `${x}.html`,
  template: `./src/pages/${x}/${x}.html`,
  favicon: `./src/pages/favicon.ico`,
}));
const scripts = ObjectFromEntries(pages.map(x => [x, `./src/pages/${x}/${x}.js`]));

function ObjectFromEntries(entries) {
  const res = {};
  for (let pair of entries) {
    res[pair[0]] = pair[1];
  }
  return res;
}

module.exports = {
  entry: {
    ...scripts,
  },
  plugins: [
    new CleanWebpackPlugin(),
    ...htmls,
  ],
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.s[ac]ss$/i,
        use: ['style-loader', 'css-loader', 'sass-loader'],
      },
      {
        test: /\.(ico|png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource',
      },
     {
       test: /\.(woff|woff2|eot|ttf|otf)$/i,
       type: 'asset/resource',
     },
    ],
  },
  output: {
    path: path.resolve(__dirname, 'build'),
  },
  optimization: {
    splitChunks: {
      chunks: "all",
    },
  },
};
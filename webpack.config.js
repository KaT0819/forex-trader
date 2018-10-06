const path = require('path');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: './frontend/index.tsx',
    output: {
        filename: '[name].bundle.js',
        chunkFilename: '[name].bundle.js',
        path: path.resolve(__dirname, 'dist'),
    },
    resolve: {
        modules: [__dirname, 'node_modules'],
        extensions: ['.ts', '.tsx', '.js'],
    },
    devtool: 'inline-source-map',
    module: {
        strictExportPresence: true,
        rules: [
            {
                test: /\.tsx?$/,
                use: [
                    { loader: 'awesome-typescript-loader' },
                ],
                exclude: /node_modules/,
            },
            {
                test: /\.css$/,
                loader: ['style-loader', 'css-loader'],
            },
            { test: /\.(png|svg)$/, loader: 'file-loader' },
            {
                test: /\.(eot|ttf|woff|woff2)$/, loader: 'file-loader',
                options: {
                    name: '[name].[ext]',
                    outputPath: 'fonts/',
                },
            },
        ],
    },
    plugins: [
        new CleanWebpackPlugin('dist'),
        new HtmlWebpackPlugin({
            template: path.resolve(__dirname, 'frontend/index.html'),
        }),
    ],
    optimization: {
        splitChunks: {
            chunks: 'all',
        },
    },
};

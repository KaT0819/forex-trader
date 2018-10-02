const path = require("path");
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: "./frontend/index.tsx",
    output: {
        path: path.resolve(__dirname, "dist"),
        filename: "index_bundle.js",
    },
    resolve: {
        extensions: [".ts", ".tsx", ".js"]
    },
    module: {
        strictExportPresence: true,
        rules: [
            {
                test: /\.tsx?$/,
                use: [
                    {loader: "awesome-typescript-loader"},
                ],
                exclude: /node_modules/,
            },
            {
                test: /\.ejs$/,
                loader: 'ejs-loader',
                query: {
                    interpolate: /{{(.+?)}}/g,
                    evaluate: /\[\[(.+?)]]/g
                },
                exclude: /node_modules/,
            },
        ],
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: path.resolve(__dirname, "frontend/index.html"),
        })
    ]
};

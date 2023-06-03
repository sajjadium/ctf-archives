const webpack = require('webpack');
const path = require('path');
const ReactRefreshWebpackPlugin = require('@pmmmwh/react-refresh-webpack-plugin');
const ReactRefreshTypeScript = require('react-refresh-typescript');
const TerserPlugin = require("terser-webpack-plugin");

const isDevelopment = process.env.NODE_ENV !== 'production';

const config = {
    mode: isDevelopment ? 'development' : 'production',
    entry: './client/index.ts',
    output: {
        path: path.resolve(__dirname, 'build', 'client'),
        filename: 'bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.*\.ts(x)?$/,
                include: /(share|client)\/.*\.ts(x)?$/,
                loader: 'ts-loader',
                exclude: /node_modules/,
                options: {
                    getCustomTransformers: () => ({
                        before: [isDevelopment && ReactRefreshTypeScript()].filter(Boolean),
                    }),
                    transpileOnly: isDevelopment,
                    configFile: "tsconfig.webpack.json"
                }
            },
            {
                test: /\.css$/i,
                use: ["style-loader", "css-loader"],
            },
            {
                test: /\.glsl$/,
                type: 'asset/source',
            }
        ]
    },
    plugins: [isDevelopment && new ReactRefreshWebpackPlugin()].filter(Boolean),
    resolve: {
        extensions: [
            '.tsx',
            '.ts',
            '.js'
        ]
    },
    devServer: {
        hot: true,
        static: {
            directory: path.join(__dirname, 'assets', 'static'),
        }
    },
    optimization: {
        minimize: true,
        minimizer: [new TerserPlugin({
            terserOptions: {
                keep_classnames: true
            }
        })],
    }
};

module.exports = config;

// Load configuration from environment or config file
const path = require('path');
const CompressionPlugin = require('compression-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

// Environment variable overrides
const config = {
  disableHotReload: process.env.DISABLE_HOT_RELOAD === 'true',
};

module.exports = {
  webpack: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
    configure: (webpackConfig, { env, paths }) => {
      
      // Production optimizations
      if (env === 'production') {
        // Enable compression for all text assets
        webpackConfig.plugins.push(
          new CompressionPlugin({
            test: /\.(js|css|html|svg)$/,
            algorithm: 'gzip',
            threshold: 8192,
            minRatio: 0.8,
          })
        );

        // Optimize bundle splitting for better caching
        webpackConfig.optimization = {
          ...webpackConfig.optimization,
          splitChunks: {
            chunks: 'all',
            minSize: 20000,
            maxSize: 250000,
            cacheGroups: {
              default: {
                minChunks: 2,
                priority: -20,
                reuseExistingChunk: true,
              },
              vendor: {
                test: /[\\/]node_modules[\\/]/,
                name: 'vendors',
                chunks: 'all',
                priority: 10,
                enforce: true,
              },
              common: {
                name: 'common',
                minChunks: 2,
                chunks: 'all',
                priority: 5,
                reuseExistingChunk: true,
              },
              // Separate chunk for large libraries
              react: {
                test: /[\\/]node_modules[\\/](react|react-dom)[\\/]/,
                name: 'react',
                chunks: 'all',
                priority: 15,
              },
              // Icons and UI libraries
              icons: {
                test: /[\\/]node_modules[\\/](lucide-react|@heroicons)[\\/]/,
                name: 'icons',
                chunks: 'all',
                priority: 12,
              },
              // Chart and visualization libraries
              charts: {
                test: /[\\/]node_modules[\\/](recharts|d3|chart\.js)[\\/]/,
                name: 'charts',
                chunks: 'all',
                priority: 12,
              }
            },
          },
          minimizer: [
            new TerserPlugin({
              terserOptions: {
                compress: {
                  drop_console: true, // Remove console.logs in production
                  drop_debugger: true,
                  pure_funcs: ['console.log', 'console.info', 'console.debug'], // Remove specific console methods
                  dead_code: true,
                  unused: true,
                },
                mangle: {
                  safari10: true,
                },
                format: {
                  comments: false,
                },
              },
              extractComments: false,
            }),
            new CssMinimizerPlugin({
              minimizerOptions: {
                preset: [
                  "default",
                  {
                    discardComments: { removeAll: true },
                    normalizeWhitespace: true,
                    colormin: true,
                    convertValues: true,
                    discardDuplicates: true,
                    discardEmpty: true,
                    mergeRules: true,
                    minifySelectors: true,
                  },
                ],
              },
            }),
          ],
        };

        // Enable tree shaking for better dead code elimination
        webpackConfig.mode = 'production';
        webpackConfig.optimization.usedExports = true;
        webpackConfig.optimization.providedExports = true;
        webpackConfig.optimization.sideEffects = false;

        // Add performance hints
        webpackConfig.performance = {
          hints: 'warning',
          maxEntrypointSize: 512000,
          maxAssetSize: 512000,
        };

        // Preload and prefetch optimization
        webpackConfig.optimization.runtimeChunk = {
          name: 'runtime',
        };
      }

      // Development optimizations
      if (env === 'development') {
        // Faster builds in development
        webpackConfig.optimization = {
          ...webpackConfig.optimization,
          removeAvailableModules: false,
          removeEmptyChunks: false,
          splitChunks: false,
        };

        // Faster source maps for development
        webpackConfig.devtool = 'eval-cheap-module-source-map';
      }
      
      // Disable hot reload completely if environment variable is set
      if (config.disableHotReload) {
        // Remove hot reload related plugins
        webpackConfig.plugins = webpackConfig.plugins.filter(plugin => {
          return !(plugin.constructor.name === 'HotModuleReplacementPlugin');
        });
        
        // Disable watch mode
        webpackConfig.watch = false;
        webpackConfig.watchOptions = {
          ignored: /.*/, // Ignore all files
        };
      } else {
        // Add ignored patterns to reduce watched directories
        webpackConfig.watchOptions = {
          ...webpackConfig.watchOptions,
          ignored: [
            '**/node_modules/**',
            '**/.git/**',
            '**/build/**',
            '**/dist/**',
            '**/coverage/**',
            '**/public/**',
          ],
          aggregateTimeout: 300,
          poll: 1000,
        };
      }

      // Add module resolution optimizations
      webpackConfig.resolve = {
        ...webpackConfig.resolve,
        modules: ['node_modules', path.resolve(__dirname, 'src')],
        symlinks: false,
        cacheWithContext: false,
      };

      // Add loader optimizations
      const oneOfRule = webpackConfig.module.rules.find(rule => rule.oneOf);
      if (oneOfRule) {
        oneOfRule.oneOf.forEach(rule => {
          if (rule.test && rule.test.toString().includes('jsx?')) {
            rule.include = path.resolve(__dirname, 'src');
            rule.exclude = /node_modules/;
          }
        });
      }
      
      return webpackConfig;
    },
  },
  devServer: {
    port: 3000,
    compress: true,
    historyApiFallback: true,
    hot: !config.disableHotReload,
    client: {
      overlay: {
        errors: true,
        warnings: false,
      },
    },
  },
};
module.exports = {
  devServer: {
    proxy: {
      '^/api/': {
        target: 'http://webserver:5000',
        secure: false,
        changeOrigin: true,
      },
    },
  },
  lintOnSave: false, 
};

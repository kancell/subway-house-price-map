module.exports = {
    // ...
    css: {
        loaderOptions: {
          less: {
            javascriptEnabled: true
          }
        }
      },
    configureWebpack(config) {
        // ...

        config.externals = {
            'AMap': 'AMap' // 高德地图配置
        }
    }
    
}
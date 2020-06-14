module.exports = {
    // ...
    chainWebpack: config => {
      config
        .plugin('html')
        .tap(args => {
          args[0].title= '房价热力地图'
          return args
        })
    },
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
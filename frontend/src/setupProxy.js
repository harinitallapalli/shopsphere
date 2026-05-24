const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/auth-api",
    createProxyMiddleware({
      target: "http://127.0.0.1:5001",
      changeOrigin: true,
      pathRewrite: { "^/auth-api": "" },
    })
  );

  app.use(
    "/product-api",
    createProxyMiddleware({
      target: "http://127.0.0.1:8001",
      changeOrigin: true,
      pathRewrite: { "^/product-api": "" },
    })
  );

  app.use(
    "/order-api",
    createProxyMiddleware({
      target: "http://127.0.0.1:8002",
      changeOrigin: true,
      pathRewrite: { "^/order-api": "" },
    })
  );
};

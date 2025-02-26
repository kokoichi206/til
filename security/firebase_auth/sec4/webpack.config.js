const CopyPlugin = require("copy-webpack-plugin");

module.exports = () => {
  const config = {
    mode: "production",
    entry: {
      login: "./src/js/login.js",
      mypage: "./src/js/mypage.js",
      "register-email": "./src/js/register-email.js",
      recovery: "./src/js/recovery.js",
    },
    output: {
      path: `${__dirname}/public`,
      filename: "[name].bundle.js",
    },
    plugins: [
      new CopyPlugin({
        patterns: [
          {
            from: `${__dirname}/src/html`,
            to: `${__dirname}/public`,
          },
          {
            from: `${__dirname}/src/style.css`,
            to: `${__dirname}/public`,
          },
        ],
      }),
    ],
  };

  return config;
};

module.exports = {
  async redirects() {
    return [
      {
        source: "/join",
        destination: "https://discord.gg/AaMz4gp",
        permanent: true,
      },
    ];
  },
  withTM() {
    require("next-transpile-modules")([
      "@amcharts/amcharts4/core",
      "@amcharts/amcharts4/themes/animated",
      "@amcharts/amcharts4/plugins/forceDirected",
      "@amcharts/amcharts4/themes/dark",
    ]); // pass the modules you would like to see transpiled
  },
};

const next_config = {
  async redirects() {
    return [
      {
        source: "/join",
        destination: "https://discord.gg/AaMz4gp",
        permanent: true,
      },
    ];
  },
};
const withTM = () => require("next-transpile-modules")(["@amcharts/amcharts4"]); // pass the modules you would like to see transpiled

module.exports = withTM(next_config);

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
};

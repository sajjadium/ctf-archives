/** @type {import('next').NextConfig} */
const nextConfig = {
  // productionBrowserSourceMaps: true,
  experimental: {
    serverActions: true,
  },
};

module.exports = nextConfig;

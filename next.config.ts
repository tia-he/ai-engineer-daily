import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/search",
        destination: "http://127.0.0.1:8000/search",
      },
    ];
  },
};

export default nextConfig;

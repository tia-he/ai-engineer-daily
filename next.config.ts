import type { NextConfig } from "next";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/search",
        destination: `${API_BASE_URL}/search`,
      },
    ];
  },
};

export default nextConfig;

import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Consume @hunterseeker/shared straight from its TypeScript source; no build step.
  transpilePackages: ["@hunterseeker/shared"],
  async redirects() {
    return [
      // The Seeker home is `/` (#9). `/seeker` stays as a permanent alias so the interim
      // persona redirect from login (#7) keeps working.
      { source: "/seeker", destination: "/", permanent: true },
    ];
  },
};

export default nextConfig;

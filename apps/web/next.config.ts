import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Consume @hunterseeker/shared straight from its TypeScript source; no build step.
  transpilePackages: ["@hunterseeker/shared"],
};

export default nextConfig;

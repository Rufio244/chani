const nextConfig = {
  reactStrictMode: true,

  // เปิดให้ใช้ API + server actions ได้ดีขึ้น
  experimental: {
    serverActions: true,
  },

  // ปรับสำหรับ deploy บน Vercel
  poweredByHeader: false,

  // ป้องกันปัญหา build กับ external modules (AI / SDK)
  serverExternalPackages: ["openai"],

  // security headers พื้นฐาน
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          {
            key: "X-Content-Type-Options",
            value: "nosniff",
          },
          {
            key: "X-Frame-Options",
            value: "DENY",
          },
          {
            key: "X-XSS-Protection",
            value: "1; mode=block",
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;

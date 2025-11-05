import type { NextConfig } from "next";
import createMDX from "@next/mdx";

const nextConfig: NextConfig = {
  // 静的出力設定（GitHub Pages用）
  output: "export",
  trailingSlash: true,
  images: {
    unoptimized: true, // GitHub Pages 必須
  },

  // basePath（GitHub Pagesのリポジトリ名に合わせて設定）
  basePath:
    process.env.NODE_ENV === "production" ? "/YUNACAMI.GITHUB.IO" : "",

  pageExtensions: ["mdx", "ts", "tsx"],

  // 🔹 redirects は静的環境でも安全に動くように固定値で設定
  async redirects() {
    return [
      // 例: "/old" → "/new" にリダイレクト
      // { source: "/old", destination: "/new", permanent: true },
    ];
  },

  experimental: {
    mdxRs: true,
  },
};

const withMDX = createMDX({});
export default withMDX(nextConfig);

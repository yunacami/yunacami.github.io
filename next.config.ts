import type { NextConfig } from "next";
import createMDX from "@next/mdx";

const withMDX = createMDX({
  // 可选：支持 .md/.mdx 文件导入
  extension: /\.mdx?$/,
});

const nextConfig: NextConfig = {
  // 为静态导出启用 export 模式
  output: "export",

  // GitHub Pages 必须加 trailingSlash
  trailingSlash: true,

  // GitHub Pages 不支持 Next.js 的图片优化
  images: {
    unoptimized: true,
  },

  // 👇 如果你的仓库名是 YUNACAMI.GITHUB.IO，留空即可
  // 如果你的仓库名是别的，比如 my-next-site，就要写 "/my-next-site"
  basePath: process.env.NODE_ENV === "production" ? "/YUNACAMI.GITHUB.IO" : "",

  // 页面扩展名支持
  pageExtensions: ["ts", "tsx", "mdx"],

  // 不需要 redirects（静态导出不支持）
  async redirects() {
    return [];
  },

  experimental: {
    mdxRs: true,
  },
};

export default withMDX(nextConfig);

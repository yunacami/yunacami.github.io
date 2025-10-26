import type { NextConfig } from "next";
import createMDX from "@next/mdx";

const nextConfig: NextConfig = {
  // 添加静态导出配置
  output: "export",
  trailingSlash: true,
  images: {
    unoptimized: true, // GitHub Pages 需要这个配置
  },

  // 基础路径配置（重要！）
  basePath: process.env.NODE_ENV === "production" ? "/YUNACAMI.GITHUB.IO" : "",
  // 或者如果你的仓库名就是 yunacami.github.io，则使用：
  // basePath: process.env.NODE_ENV === 'production' ? '' : '',

  pageExtensions: ["mdx", "ts", "tsx"],

  // 移除或修改异步重定向（静态导出不支持异步操作）
  async redirects() {
    // 静态导出时跳过数据库查询
    if (!process.env.POSTGRES_URL || process.env.NODE_ENV === "production") {
      return [];
    }

    // 开发环境保持原有逻辑
    const { sql } = await import("./lib/database"); // 需要调整导入方式
    let redirects = await sql`
      SELECT source, destination, permanent
      FROM redirects;
    `;

    return redirects.map(({ source, destination, permanent }) => ({
      source,
      destination,
      permanent: !!permanent,
    }));
  },

  experimental: {
    mdxRs: true,
  },
};

const withMDX = createMDX({});
export default withMDX(nextConfig);

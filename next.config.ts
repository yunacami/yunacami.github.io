import type { NextConfig } from "next";
import createMDX from "@next/mdx";

const withMDX = createMDX({
  // 必要に応じて markdown プラグインを追加
  // remarkPlugins: [],
  // rehypePlugins: [],
});

const nextConfig: NextConfig = {
  // `.md` と `.mdx` を Next.js のページ拡張子として認識させる
  pageExtensions: ["js", "jsx", "md", "mdx", "ts", "tsx"],

  // 追加の Next.js 設定があればここに記述
  // reactStrictMode: true,
};

// MDX 設定を Next.js 設定にマージしてエクスポート
export default withMDX(nextConfig);

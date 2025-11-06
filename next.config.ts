import type { NextConfig } from 'next'
import createMDX from '@next/mdx'

const withMDX = createMDX({
  // .md および .mdx ファイルをサポート
  extension: /\.(md|mdx)$/,
})

const nextConfig: NextConfig = {
  // markdown / mdx ファイルを page として扱う
  pageExtensions: ['js', 'jsx', 'md', 'mdx', 'ts', 'tsx'],
  // ほかの Next.js 設定をここに追加可能
}

// MDX 設定をマージしてエクスポート
export default withMDX(nextConfig)

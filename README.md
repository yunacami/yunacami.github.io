# 全球财经早报

个人财经信息网站：<https://yunacami.github.io>

每天**东京时间早上 7:00**（UTC 22:00），GitHub Actions 自动运行：

1. `scripts/generate_report.py` 调用 Claude（结合实时网络搜索 + 主流财经媒体 RSS 头条）总结近期全球财经信息，生成一篇 Markdown 早报写入 `_posts/`；
2. 自动提交到 `main` 分支；
3. 用 Jekyll 构建并部署到 GitHub Pages。

## 仓库结构

| 路径 | 说明 |
|---|---|
| `_posts/` | 每日早报（自动生成） |
| `scripts/generate_report.py` | 早报生成脚本 |
| `.github/workflows/daily-report.yml` | 每日定时：生成 → 提交 → 构建 → 部署 |
| `.github/workflows/deploy.yml` | push 到 main 时构建并部署 |
| `_config.yml` | Jekyll 配置（minima 主题） |

## 启用前的两步配置

1. **API Key**：仓库 Settings → Secrets and variables → Actions → 新建 secret `ANTHROPIC_API_KEY`（值为你的 Anthropic API key）。未配置时早报退化为各媒体 RSS 头条摘要。
2. **Pages 来源**：仓库 Settings → Pages → Build and deployment → Source 选择 **GitHub Actions**。

## 手动触发

Actions 页面选择 "Daily Finance Report" → Run workflow，可立即生成当天早报。

> 内容由 AI 自动生成，仅供个人参考，不构成投资建议。

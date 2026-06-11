#!/usr/bin/env python3
"""生成每日全球财经早报，写入 _posts/ 目录。

- 设置了 ANTHROPIC_API_KEY 时：调用 Claude（带网络搜索）生成中文财经总结。
- 未设置时：抓取主流财经媒体 RSS，生成头条摘要，保证站点照常更新。
"""

import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

JST = timezone(timedelta(hours=9))
POSTS_DIR = Path(__file__).resolve().parent.parent / "_posts"

RSS_FEEDS = [
    ("BBC Business", "https://feeds.bbci.co.uk/news/business/rss.xml"),
    ("CNBC Top News", "https://www.cnbc.com/id/100003114/device/rss/rss.html"),
    ("MarketWatch", "https://feeds.content.dowjones.io/public/rss/mw_topstories"),
    ("Nikkei Asia", "https://asia.nikkei.com/rss/feed/nar"),
]


def fetch_headlines(max_per_feed: int = 10) -> dict[str, list[tuple[str, str]]]:
    headlines: dict[str, list[tuple[str, str]]] = {}
    for source, url in RSS_FEEDS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                root = ET.fromstring(resp.read())
            items = []
            for item in root.iter("item"):
                title = (item.findtext("title") or "").strip()
                link = (item.findtext("link") or "").strip()
                if title:
                    items.append((title, link))
                if len(items) >= max_per_feed:
                    break
            if items:
                headlines[source] = items
        except Exception as e:  # 单个源失败不影响整体
            print(f"[warn] fetch {source} failed: {e}", file=sys.stderr)
    return headlines


def summarize_with_claude(date_str: str, headlines: dict) -> str:
    from anthropic import Anthropic

    client = Anthropic()

    headline_text = "\n".join(
        f"- [{source}] {title}" for source, items in headlines.items() for title, _ in items
    ) or "（RSS 头条抓取失败，请完全依靠网络搜索）"

    prompt = f"""今天是 {date_str}（东京时间）。请你作为一名资深财经分析师，为一位特定读者写一篇当日的《全球财经早报》，用简体中文、Markdown 格式输出。

读者画像：从事留学行业（关注汇率、各国签证/教育/移民政策、中产家庭消费力），同时在积极挖掘其他行业的创业与转型机会。时间有限，需要快速消化吸收——所以每条信息都要回答"这意味着什么"，而不是单纯罗列新闻。

请先使用网络搜索补充最新信息（过去 24-48 小时的全球财经新闻、主要指数收盘情况、大宗商品与汇率走势、各国教育/签证政策动向等），再结合下面抓取到的媒体头条进行写作。

参考头条：
{headline_text}

按以下小节组织（用二级标题 ##）：

## 今日要点
3-5 条 TL;DR，每条一句话新闻 + 一句话"为什么重要"。读者只看这一节也能掌握当天大局。

## 市场与宏观
美股/欧股/亚太主要指数表现、央行与重要经济数据。不要只报数字——说明背后的驱动因素，以及对后市的含义。

## 汇率与大宗商品
重点关注美元、日元、人民币、英镑、加元、澳元、欧元的走势（这些直接影响留学成本），其次是原油黄金。给出具体变动幅度并解读趋势。

## 留学行业视角
当天新闻中与留学行业相关的信号：汇率变化对各目的地留学成本的影响、主要留学目的国（美英加澳日等）的签证/教育/移民政策动向、中国宏观经济与中产消费力变化对留学需求的影响、教育类公司动态。如果当天没有直接相关新闻，从汇率和宏观角度做简短推演即可，不要硬凑。

## 机会雷达
从当天新闻中提炼 1-3 个值得关注的行业趋势或潜在机会（新兴行业、政策红利、资金流向、技术拐点等），每个说明：信号是什么、为什么值得关注、适合什么样的切入方式。面向正在探索新方向的个人创业者/从业者，不要泛泛而谈。

## 今日关注
当日值得留意的财经事件、数据发布或政策节点。

写作要求：
1. 客观准确，数字给出具体涨跌幅；分析与事实分开，推测性判断明确标注"分析"或"推测"；不确定的信息注明"待确认"。
2. 总长度 1500-2500 字。分析要具体、可操作，避免"值得持续关注"这类空话。
3. 直接输出正文 Markdown，不要输出 YAML front matter，不要以一级标题开头（标题由系统添加）。
4. 结尾加一行斜体免责声明：*本文由 AI 自动生成，不构成投资建议。*"""

    with client.messages.stream(
        model="claude-opus-4-8",
        max_tokens=20000,
        thinking={"type": "adaptive"},
        tools=[{"type": "web_search_20260209", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        message = stream.get_final_message()

    return "\n".join(b.text for b in message.content if b.type == "text").strip()


def fallback_digest(headlines: dict) -> str:
    if not headlines:
        return "今日头条抓取失败，暂无内容。\n"
    parts = ["> 未配置 ANTHROPIC_API_KEY，以下为各财经媒体头条摘要。\n"]
    for source, items in headlines.items():
        parts.append(f"## {source}\n")
        parts.extend(f"- [{title}]({link})" for title, link in items)
        parts.append("")
    return "\n".join(parts)


def main() -> None:
    now = datetime.now(JST)
    date_str = now.strftime("%Y-%m-%d")

    headlines = fetch_headlines()

    if os.environ.get("ANTHROPIC_API_KEY"):
        body = summarize_with_claude(date_str, headlines)
    else:
        print("[warn] ANTHROPIC_API_KEY 未设置，使用 RSS 头条摘要模式", file=sys.stderr)
        body = fallback_digest(headlines)

    POSTS_DIR.mkdir(exist_ok=True)
    post_path = POSTS_DIR / f"{date_str}-finance-daily.md"
    front_matter = (
        "---\n"
        "layout: post\n"
        f'title: "全球财经早报 · {date_str}"\n'
        f"date: {now.strftime('%Y-%m-%d %H:%M:%S')} +0900\n"
        "categories: daily\n"
        "---\n\n"
    )
    post_path.write_text(front_matter + body + "\n", encoding="utf-8")
    print(f"written: {post_path}")


if __name__ == "__main__":
    main()

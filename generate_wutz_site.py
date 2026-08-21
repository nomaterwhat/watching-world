#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Infinite Challenge viewing catalog website from JSON data."""

import json
import html

def main():
    with open(r'C:\Users\hkb\.qianfan\workspace\a4256da5e8944f22b58659270dd2e291\wutz_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_cats = data['left_categories'] + data['right_categories']
    member_timeline = data['member_timeline']

    # Collect stats
    total_eps = sum(len(c['items']) for c in all_cats)
    total_cats = len(all_cats)

    # Collect all unique years
    all_years_set = set()
    for cat in all_cats:
        for item in cat['items']:
            if item['year']:
                all_years_set.add(item['year'])
    all_years = sorted(all_years_set)

    # Year stats
    year_stats = {}
    for cat in all_cats:
        for item in cat['items']:
            y = item['year'] or '未知'
            year_stats[y] = year_stats.get(y, 0) + 1

    # Generate category cards HTML
    cat_cards_html = ""
    for i, cat in enumerate(all_cats):
        cat_name_escaped = html.escape(cat['name'])
        ep_count = len(cat['items'])

        # Group episodes by year within category
        year_groups = {}
        for item in cat['items']:
            y = item['year'] or '未知'
            if y not in year_groups:
                year_groups[y] = []
            year_groups[y].append(item['title'])

        # Build episode list HTML
        eps_html = ""
        for year in sorted(year_groups.keys()):
            eps = year_groups[year]
            eps_html += f'<div class="ep-year-group">\n'
            eps_html += f'  <span class="ep-year-tag">{html.escape(year)}</span>\n'
            eps_html += f'  <div class="ep-list">\n'
            for ep_title in eps:
                title_escaped = html.escape(ep_title)
                eps_html += f'    <div class="ep-item" data-title="{title_escaped.lower()}">{title_escaped}</div>\n'
            eps_html += f'  </div>\n'
            eps_html += f'</div>\n'

        cat_cards_html += f'''
        <div class="cat-card reveal" data-cat="{cat_name_escaped}" data-eps="{ep_count}">
          <div class="cat-header">
            <h3 class="cat-name">{cat_name_escaped}</h3>
            <span class="cat-count">{ep_count} 集</span>
          </div>
          <div class="cat-body">
            {eps_html}
          </div>
        </div>
        '''

    # Generate filter buttons
    filter_btns_html = '<button class="filter-btn active" data-filter="all">全部</button>\n'
    for cat in all_cats:
        name = html.escape(cat['name'])
        filter_btns_html += f'          <button class="filter-btn" data-filter="{name}">{name}</button>\n'

    # Generate year stats HTML
    year_bars_html = ""
    max_count = max(year_stats.values())
    for year in sorted(year_stats.keys()):
        count = year_stats[year]
        pct = int(count / max_count * 100)
        year_bars_html += f'''
            <div class="year-bar-item">
              <span class="year-bar-label">{html.escape(year)}</span>
              <div class="year-bar-track"><div class="year-bar-fill" data-width="{pct}"></div></div>
              <span class="year-bar-count">{count}</span>
            </div>
            '''

    # Generate member timeline HTML
    # Split into events (rows 1-16) and periods (rows 18-31)
    events = []
    periods = []
    for entry in member_timeline:
        if entry.startswith(('第一次', '第二次', '第三次', '第四次', '第五次', '第六次')):
            periods.append(entry)
        elif entry == '1.不同成员时期':
            continue
        else:
            events.append(entry)

    timeline_events_html = ""
    for event in events:
        timeline_events_html += f'''
          <div class="tl-item">
            <div class="tl-dot"></div>
            <div class="tl-content">{html.escape(event)}</div>
          </div>
          '''

    timeline_periods_html = ""
    for period in periods:
        timeline_periods_html += f'<div class="period-tag">{html.escape(period)}</div>\n'

    # Generate full HTML
    full_html = f'''<!DOCTYPE html>
<html lang="zh-CN" data-theme="minimal">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="无限挑战观看目录 - 622集节目完整索引，39个特辑分类，2005-2018">
<title>无限挑战观看目录</title>
<style>
:root {{
  --transition-theme: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-fast: 0.2s ease;
  --transition-base: 0.3s ease;
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-full: 9999px;
  --max-width: 1200px;
  --nav-height: 60px;
  --font-base: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
  --font-mono: "SF Mono", "Fira Code", Consolas, monospace;
}}

/* Theme 1: Minimal */
[data-theme="minimal"] {{
  --bg: #f8f9fa; --bg-2: #fff; --bg-3: #f1f3f5;
  --text: #1a1a2e; --text-2: #6c757d; --text-3: #adb5bd;
  --accent: #3b82f6; --accent-h: #2563eb; --accent-soft: rgba(59,130,246,0.1);
  --border: #e9ecef; --card-bg: #fff; --card-border: #e9ecef;
  --shadow: 0 2px 12px rgba(0,0,0,0.06); --shadow-hover: 0 8px 30px rgba(0,0,0,0.12);
  --shadow-accent: 0 4px 20px rgba(59,130,246,0.2);
  --hero-grad: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%);
  --nav-bg: rgba(255,255,255,0.85); --nav-border: rgba(0,0,0,0.06);
  --tag-bg: #f1f3f5; --tag-text: #495057;
  --font-h: var(--font-base);
}}
/* Theme 2: DarkTech */
[data-theme="darktech"] {{
  --bg: #0a0e1a; --bg-2: #131826; --bg-3: #1a2033;
  --text: #e2e8f0; --text-2: #94a3b8; --text-3: #64748b;
  --accent: #00ff9d; --accent-h: #00cc7d; --accent-soft: rgba(0,255,157,0.08);
  --border: #1e293b; --card-bg: #131826; --card-border: #1e293b;
  --shadow: 0 2px 12px rgba(0,0,0,0.4); --shadow-hover: 0 8px 30px rgba(0,255,157,0.1);
  --shadow-accent: 0 0 24px rgba(0,255,157,0.25);
  --hero-grad: linear-gradient(135deg, #0a0e1a 0%, #0d1521 50%, #0a1f1a 100%);
  --nav-bg: rgba(10,14,26,0.85); --nav-border: rgba(0,255,157,0.1);
  --tag-bg: rgba(0,255,157,0.08); --tag-text: #00ff9d;
  --font-h: var(--font-mono);
}}
/* Theme 3: Creative */
[data-theme="creative"] {{
  --bg: #fef3ff; --bg-2: #fff; --bg-3: #f3e8ff;
  --text: #2d1b4e; --text-2: #7c6a9c; --text-3: #b4a3c8;
  --accent: #a855f7; --accent-h: #9333ea; --accent-soft: rgba(168,85,247,0.1);
  --border: #f3e8ff; --card-bg: #fff; --card-border: #f3e8ff;
  --shadow: 0 4px 16px rgba(168,85,247,0.08); --shadow-hover: 0 12px 36px rgba(168,85,247,0.18);
  --shadow-accent: 0 4px 24px rgba(236,72,153,0.25);
  --hero-grad: linear-gradient(135deg, #fef3ff 0%, #fce7f3 50%, #ddd6fe 100%);
  --nav-bg: rgba(254,243,255,0.85); --nav-border: rgba(168,85,247,0.1);
  --tag-bg: #f3e8ff; --tag-text: #7c3aed;
  --font-h: var(--font-base);
}}
/* Theme 4: GuoFeng */
[data-theme="guofeng"] {{
  --bg: #f5f0e8; --bg-2: #ede4d3; --bg-3: #e8dcc6;
  --text: #2c1810; --text-2: #6b4423; --text-3: #a08968;
  --accent: #8b2500; --accent-h: #6b1d00; --accent-soft: rgba(139,37,0,0.08);
  --border: #d4c4a8; --card-bg: #faf6ef; --card-border: #d4c4a8;
  --shadow: 0 2px 12px rgba(139,37,0,0.06); --shadow-hover: 0 8px 30px rgba(139,37,0,0.12);
  --shadow-accent: 0 4px 20px rgba(212,160,23,0.2);
  --hero-grad: linear-gradient(135deg, #f5f0e8 0%, #ede4d3 50%, #f0e6d2 100%);
  --nav-bg: rgba(245,240,232,0.88); --nav-border: rgba(139,37,0,0.08);
  --tag-bg: #ede4d3; --tag-text: #8b2500;
  --font-h: "Songti SC", "STSong", serif;
}}
/* Theme 5: HandDrawn */
[data-theme="handdrawn"] {{
  --bg: #fdf6e3; --bg-2: #f5ecd7; --bg-3: #efe4c8;
  --text: #3c2f1f; --text-2: #8b6914; --text-3: #bda56a;
  --accent: #d97706; --accent-h: #b45309; --accent-soft: rgba(217,119,6,0.1);
  --border: #e7d5b5; --card-bg: #fffbeb; --card-border: #e7d5b5;
  --shadow: 0 2px 8px rgba(139,105,20,0.08); --shadow-hover: 0 8px 24px rgba(139,105,20,0.15);
  --shadow-accent: 0 4px 20px rgba(217,119,6,0.2);
  --hero-grad: linear-gradient(135deg, #fdf6e3 0%, #faecd0 50%, #f5e6c8 100%);
  --nav-bg: rgba(253,246,227,0.88); --nav-border: rgba(139,105,20,0.08);
  --tag-bg: #f5ecd7; --tag-text: #8b6914;
  --font-h: "Hannotate SC", "Comic Sans MS", cursive;
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; scroll-padding-top: calc(var(--nav-height) + 20px); }}
body {{
  font-family: var(--font-base); background: var(--bg); color: var(--text);
  line-height: 1.7; transition: background var(--transition-theme), color var(--transition-theme);
  overflow-x: hidden;
}}
h1,h2,h3,h4 {{ font-family: var(--font-h); font-weight: 700; line-height: 1.3; color: var(--text); transition: color var(--transition-theme); }}
a {{ color: var(--accent); text-decoration: none; transition: color var(--transition-fast); }}
a:hover {{ color: var(--accent-h); }}
button {{ font-family: inherit; cursor: pointer; border: none; background: none; }}
ul,ol {{ list-style: none; }}
section {{ padding: 70px 0; position: relative; }}
.container {{ max-width: var(--max-width); margin: 0 auto; padding: 0 24px; }}

/* Navbar */
.navbar {{
  position: fixed; top: 0; left: 0; right: 0; height: var(--nav-height);
  background: var(--nav-bg); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--nav-border); z-index: 1000;
  transition: background var(--transition-theme), border-color var(--transition-theme);
}}
.navbar .container {{ height: 100%; display: flex; align-items: center; justify-content: space-between; }}
.nav-logo {{
  font-family: var(--font-h); font-size: 18px; font-weight: 800; color: var(--text);
  display: flex; align-items: center; gap: 8px; transition: color var(--transition-theme);
}}
.nav-logo-mark {{
  width: 30px; height: 30px; border-radius: var(--radius-sm);
  background: var(--accent); display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 14px; transition: background var(--transition-theme);
}}
.nav-links {{ display: flex; align-items: center; gap: 4px; }}
.nav-link {{
  padding: 8px 14px; font-size: 14px; color: var(--text-secondary, var(--text-2));
  border-radius: var(--radius-sm); transition: all var(--transition-fast); position: relative;
}}
.nav-link:hover {{ color: var(--text); background: var(--accent-soft); }}
.nav-link.active {{ color: var(--accent); font-weight: 600; }}
.nav-link.active::after {{
  content: ''; position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%);
  width: 20px; height: 2px; background: var(--accent); border-radius: 2px;
}}

/* Theme switcher */
.theme-switcher {{
  display: flex; align-items: center; gap: 5px; padding: 3px;
  background: var(--bg-3); border-radius: var(--radius-full); border: 1px solid var(--border);
  transition: all var(--transition-theme);
}}
.theme-btn {{
  width: 26px; height: 26px; border-radius: 50%; display: flex;
  align-items: center; justify-content: center; transition: all var(--transition-fast); position: relative;
}}
.theme-btn:hover {{ transform: scale(1.15); }}
.theme-btn.active {{ transform: scale(1.1); }}
.theme-dot {{ width: 16px; height: 16px; border-radius: 50%; border: 2px solid var(--border); }}
.theme-btn[data-theme="minimal"] .theme-dot {{ background: linear-gradient(135deg, #3b82f6, #e3f2fd); }}
.theme-btn[data-theme="darktech"] .theme-dot {{ background: linear-gradient(135deg, #00ff9d, #0a0e1a); }}
.theme-btn[data-theme="creative"] .theme-dot {{ background: linear-gradient(135deg, #a855f7, #ec4899); }}
.theme-btn[data-theme="guofeng"] .theme-dot {{ background: linear-gradient(135deg, #8b2500, #d4a017); }}
.theme-btn[data-theme="handdrawn"] .theme-dot {{ background: linear-gradient(135deg, #d97706, #fdf6e3); }}
.theme-btn.active .theme-dot {{ border-color: var(--text); }}
.theme-btn::after {{
  content: attr(data-label); position: absolute; bottom: -30px; left: 50%; transform: translateX(-50%);
  font-size: 11px; color: var(--text-2); background: var(--card-bg); padding: 2px 8px;
  border-radius: 4px; white-space: nowrap; opacity: 0; pointer-events: none;
  transition: opacity var(--transition-fast); border: 1px solid var(--border);
}}
.theme-btn:hover::after {{ opacity: 1; }}

/* Mobile nav */
.nav-toggle {{ display: none; width: 40px; height: 40px; flex-direction: column; justify-content: center; align-items: center; gap: 5px; border-radius: var(--radius-sm); }}
.nav-toggle span {{ width: 20px; height: 2px; background: var(--text); border-radius: 2px; transition: all var(--transition-fast); }}
.nav-toggle.open span:nth-child(1) {{ transform: translateY(7px) rotate(45deg); }}
.nav-toggle.open span:nth-child(2) {{ opacity: 0; }}
.nav-toggle.open span:nth-child(3) {{ transform: translateY(-7px) rotate(-45deg); }}

/* Hero */
#home {{
  min-height: 70vh; display: flex; align-items: center; padding-top: var(--nav-height);
  background: var(--hero-grad); position: relative; overflow: hidden;
}}
#home::before {{
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(circle at 20% 50%, var(--accent-soft) 0%, transparent 50%),
              radial-gradient(circle at 80% 30%, var(--accent-soft) 0%, transparent 50%);
  pointer-events: none;
}}
.hero-content {{ position: relative; z-index: 2; text-align: center; width: 100%; }}
.hero-badge {{
  display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px;
  background: var(--accent-soft); color: var(--accent); border-radius: var(--radius-full);
  font-size: 13px; font-weight: 600; margin-bottom: 20px;
}}
.hero-title {{
  font-size: clamp(32px, 5vw, 52px); font-weight: 800; margin-bottom: 16px;
  background: linear-gradient(135deg, var(--text), var(--accent));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}}
.hero-sub {{ font-size: clamp(15px, 2vw, 18px); color: var(--text-2); margin-bottom: 36px; max-width: 560px; margin-left: auto; margin-right: auto; }}
.hero-stats {{ display: flex; justify-content: center; gap: 32px; flex-wrap: wrap; margin-bottom: 32px; }}
.hero-stat {{ text-align: center; }}
.hero-stat-num {{ font-family: var(--font-h); font-size: 36px; font-weight: 800; color: var(--accent); line-height: 1; }}
.hero-stat-label {{ font-size: 13px; color: var(--text-2); margin-top: 4px; }}
.hero-actions {{ display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; }}
.btn {{
  display: inline-flex; align-items: center; gap: 8px; padding: 11px 26px;
  font-size: 14px; font-weight: 600; border-radius: var(--radius-md);
  transition: all var(--transition-base); cursor: pointer; border: 2px solid transparent;
}}
.btn-primary {{ background: var(--accent); color: #fff; box-shadow: var(--shadow-accent); }}
.btn-primary:hover {{ background: var(--accent-h); transform: translateY(-2px); color: #fff; }}
.btn-outline {{ background: transparent; color: var(--text); border-color: var(--border); }}
.btn-outline:hover {{ border-color: var(--accent); color: var(--accent); background: var(--accent-soft); }}

/* Search bar */
.search-bar {{
  max-width: 600px; margin: 0 auto 32px; position: relative;
}}
.search-input {{
  width: 100%; padding: 14px 20px 14px 48px; font-size: 15px; font-family: inherit;
  background: var(--card-bg); color: var(--text); border: 1px solid var(--border);
  border-radius: var(--radius-full); transition: all var(--transition-fast); outline: none;
  box-shadow: var(--shadow);
}}
.search-input:focus {{ border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }}
.search-icon {{ position: absolute; left: 18px; top: 50%; transform: translateY(-50%); color: var(--text-3); }}
.search-result-count {{ text-align: center; font-size: 14px; color: var(--text-2); margin-bottom: 24px; }}

/* Filters */
.filters {{ display: flex; gap: 8px; margin-bottom: 32px; flex-wrap: wrap; justify-content: center; }}
.filter-btn {{
  padding: 7px 16px; font-size: 13px; font-weight: 500; color: var(--text-2);
  background: var(--tag-bg); border-radius: var(--radius-full);
  transition: all var(--transition-fast); border: 1px solid transparent;
}}
.filter-btn:hover {{ color: var(--text); }}
.filter-btn.active {{ background: var(--accent); color: #fff; }}

/* Category cards */
.cat-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 20px; }}
.cat-card {{
  background: var(--card-bg); border: 1px solid var(--card-border);
  border-radius: var(--radius-md); overflow: hidden;
  transition: all var(--transition-base); box-shadow: var(--shadow);
}}
.cat-card:hover {{ transform: translateY(-4px); box-shadow: var(--shadow-hover); border-color: var(--accent); }}
.cat-header {{
  padding: 16px 20px; display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1px solid var(--border); cursor: pointer;
}}
.cat-name {{ font-size: 17px; transition: color var(--transition-fast); }}
.cat-card:hover .cat-name {{ color: var(--accent); }}
.cat-count {{ font-size: 12px; color: var(--text-2); background: var(--tag-bg); padding: 3px 10px; border-radius: var(--radius-full); }}
.cat-body {{ padding: 16px 20px; max-height: 400px; overflow-y: auto; }}
.cat-body.collapsed {{ display: none; }}

/* Custom scrollbar */
.cat-body::-webkit-scrollbar {{ width: 5px; }}
.cat-body::-webkit-scrollbar-track {{ background: transparent; }}
.cat-body::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}
.cat-body::-webkit-scrollbar-thumb:hover {{ background: var(--accent); }}

/* Episode items */
.ep-year-group {{ margin-bottom: 14px; }}
.ep-year-group:last-child {{ margin-bottom: 0; }}
.ep-year-tag {{
  font-size: 12px; font-weight: 700; color: var(--accent);
  background: var(--accent-soft); padding: 2px 8px; border-radius: var(--radius-sm);
  margin-bottom: 6px; display: inline-block;
}}
.ep-list {{ display: flex; flex-direction: column; gap: 4px; }}
.ep-item {{
  font-size: 13px; color: var(--text-2); padding: 5px 10px;
  border-radius: var(--radius-sm); transition: all var(--transition-fast);
  line-height: 1.5;
}}
.ep-item:hover {{ background: var(--accent-soft); color: var(--accent); }}
.ep-item.hidden {{ display: none; }}

/* Year stats */
.year-stats {{ display: grid; grid-template-columns: 1fr 1fr; gap: 32px; align-items: start; }}
.year-bars {{ display: flex; flex-direction: column; gap: 12px; }}
.year-bar-item {{ display: flex; align-items: center; gap: 12px; }}
.year-bar-label {{ font-size: 13px; font-weight: 600; color: var(--text-2); width: 60px; flex-shrink: 0; }}
.year-bar-track {{ flex: 1; height: 10px; background: var(--bg-3); border-radius: var(--radius-full); overflow: hidden; }}
.year-bar-fill {{ height: 100%; background: var(--accent); border-radius: var(--radius-full); width: 0; transition: width 1s cubic-bezier(0.4,0,0.2,1); }}
[data-theme="darktech"] .year-bar-fill {{ box-shadow: 0 0 8px var(--accent); }}
[data-theme="creative"] .year-bar-fill {{ background: linear-gradient(90deg, #a855f7, #ec4899); }}
[data-theme="guofeng"] .year-bar-fill {{ background: linear-gradient(90deg, #8b2500, #d4a017); }}
.year-bar-count {{ font-size: 13px; font-weight: 700; color: var(--accent); width: 32px; text-align: right; flex-shrink: 0; }}

.year-info-card {{
  background: var(--card-bg); border: 1px solid var(--card-border);
  border-radius: var(--radius-md); padding: 24px; box-shadow: var(--shadow);
}}
.year-info-card h3 {{ font-size: 18px; margin-bottom: 16px; }}
.year-info-list {{ display: flex; flex-direction: column; gap: 10px; }}
.year-info-item {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: var(--bg-3); border-radius: var(--radius-sm); }}
.year-info-year {{ font-weight: 600; font-size: 14px; }}
.year-info-eps {{ font-size: 13px; color: var(--accent); font-weight: 700; }}

/* Member timeline */
.member-tl-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 48px; }}
.member-events {{ position: relative; }}
.member-events::before {{
  content: ''; position: absolute; left: 8px; top: 0; bottom: 0; width: 2px; background: var(--border);
}}
[data-theme="darktech"] .member-events::before {{ background: linear-gradient(to bottom, transparent, var(--accent), transparent); box-shadow: 0 0 8px var(--accent); }}
.tl-item {{ position: relative; padding-left: 32px; padding-bottom: 20px; }}
.tl-item:last-child {{ padding-bottom: 0; }}
.tl-dot {{
  position: absolute; left: 1px; top: 4px; width: 16px; height: 16px;
  border-radius: 50%; background: var(--card-bg); border: 3px solid var(--accent); z-index: 2;
  transition: all var(--transition-base);
}}
[data-theme="darktech"] .tl-dot {{ box-shadow: 0 0 10px var(--accent); }}
.tl-item:hover .tl-dot {{ transform: scale(1.2); background: var(--accent); }}
.tl-content {{
  background: var(--card-bg); border: 1px solid var(--card-border);
  border-radius: var(--radius-md); padding: 12px 16px; box-shadow: var(--shadow);
  font-size: 14px; transition: all var(--transition-base);
}}
.tl-item:hover .tl-content {{ box-shadow: var(--shadow-hover); border-color: var(--accent); transform: translateX(4px); }}

.period-list {{ display: flex; flex-direction: column; gap: 10px; }}
.period-tag {{
  padding: 10px 14px; background: var(--card-bg); border: 1px solid var(--card-border);
  border-radius: var(--radius-md); font-size: 13px; color: var(--text-2);
  border-left: 4px solid var(--accent); transition: all var(--transition-base);
  box-shadow: var(--shadow);
}}
.period-tag:hover {{ transform: translateX(4px); border-color: var(--accent); color: var(--text); }}

/* Footer */
.footer {{ background: var(--bg-3); border-top: 1px solid var(--border); padding: 32px 0; transition: all var(--transition-theme); }}
.footer .container {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; }}
.footer-text {{ font-size: 13px; color: var(--text-2); }}

/* Reveal animation */
.reveal {{ opacity: 0; transform: translateY(30px); transition: opacity 0.6s ease, transform 0.6s ease; }}
.reveal.visible {{ opacity: 1; transform: translateY(0); }}
.reveal:nth-child(2) {{ transition-delay: 0.1s; }}
.reveal:nth-child(3) {{ transition-delay: 0.2s; }}

.theme-transitioning * {{ transition: background-color 0.4s ease, color 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease !important; }}

/* Responsive */
@media (max-width: 768px) {{
  section {{ padding: 50px 0; }}
  .container {{ padding: 0 16px; }}
  .nav-links {{
    position: fixed; top: var(--nav-height); left: 0; right: 0;
    background: var(--nav-bg); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    flex-direction: column; align-items: stretch; padding: 12px; gap: 4px;
    border-bottom: 1px solid var(--nav-border); transform: translateY(-100%); opacity: 0;
    pointer-events: none; transition: all 0.3s ease;
  }}
  .nav-links.open {{ transform: translateY(0); opacity: 1; pointer-events: auto; }}
  .nav-link {{ padding: 10px 14px; font-size: 14px; }}
  .nav-link.active::after {{ display: none; }}
  .nav-toggle {{ display: flex; }}
  .theme-switcher {{ padding: 2px; gap: 3px; }}
  .theme-btn {{ width: 22px; height: 22px; }}
  .theme-dot {{ width: 13px; height: 13px; }}
  .hero-stats {{ gap: 20px; }}
  .hero-stat-num {{ font-size: 28px; }}
  .cat-grid {{ grid-template-columns: 1fr; }}
  .year-stats {{ grid-template-columns: 1fr; }}
  .member-tl-grid {{ grid-template-columns: 1fr; }}
  .filters {{ gap: 6px; }}
  .filter-btn {{ padding: 6px 12px; font-size: 12px; }}
}}
@media (max-width: 480px) {{
  .hero-stat-num {{ font-size: 24px; }}
  .hero-actions {{ flex-direction: column; align-items: center; }}
  .btn {{ width: 100%; justify-content: center; }}
}}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{ animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }}
  .reveal {{ opacity: 1; transform: none; }}
}}
:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
</style>
</head>
<body>

<nav class="navbar" role="navigation" aria-label="Main navigation">
  <div class="container">
    <a href="#home" class="nav-logo">
      <span class="nav-logo-mark">M</span>
      <span>无限挑战目录</span>
    </a>
    <ul class="nav-links" id="navLinks">
      <li><a href="#home" class="nav-link active">首页</a></li>
      <li><a href="#catalog" class="nav-link">特辑目录</a></li>
      <li><a href="#stats" class="nav-link">年份统计</a></li>
      <li><a href="#members" class="nav-link">成员变动</a></li>
    </ul>
    <div style="display:flex;align-items:center;gap:10px;">
      <div class="theme-switcher" role="group" aria-label="Theme switcher">
        <button class="theme-btn active" data-theme="minimal" data-label="简约现代" aria-label="Minimal theme"><span class="theme-dot"></span></button>
        <button class="theme-btn" data-theme="darktech" data-label="暗黑科技" aria-label="Dark tech theme"><span class="theme-dot"></span></button>
        <button class="theme-btn" data-theme="creative" data-label="活泼创意" aria-label="Creative theme"><span class="theme-dot"></span></button>
        <button class="theme-btn" data-theme="guofeng" data-label="国风雅韵" aria-label="Guofeng theme"><span class="theme-dot"></span></button>
        <button class="theme-btn" data-theme="handdrawn" data-label="手绘温暖" aria-label="Handdrawn theme"><span class="theme-dot"></span></button>
      </div>
      <button class="nav-toggle" id="navToggle" aria-label="Toggle menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</nav>

<section id="home">
  <div class="container">
    <div class="hero-content">
      <div class="hero-badge">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
        2005 - 2018 完整观看目录
      </div>
      <h1 class="hero-title">无限挑战观看目录</h1>
      <p class="hero-sub">韩国 MBC 综艺节目《无限挑战》的完整观看索引，按特辑类别和年份分类整理。</p>
      <div class="hero-stats">
        <div class="hero-stat"><div class="hero-stat-num">{total_eps}</div><div class="hero-stat-label">集数</div></div>
        <div class="hero-stat"><div class="hero-stat-num">{total_cats}</div><div class="hero-stat-label">特辑分类</div></div>
        <div class="hero-stat"><div class="hero-stat-num">13</div><div class="hero-stat-label">年份跨度</div></div>
        <div class="hero-stat"><div class="hero-stat-num">5</div><div class="hero-stat-label">主题风格</div></div>
      </div>
      <div class="hero-actions">
        <a href="#catalog" class="btn btn-primary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/></svg>
          浏览目录
        </a>
        <a href="#stats" class="btn btn-outline">查看统计</a>
      </div>
    </div>
  </div>
</section>

<section id="catalog">
  <div class="container">
    <div class="reveal">
      <span class="section-tag" style="display:inline-block;font-size:13px;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;">CATALOG</span>
      <h2 class="section-title" style="font-size:clamp(26px,4vw,36px);margin-bottom:16px;">特辑目录</h2>
      <p style="font-size:16px;color:var(--text-2);max-width:600px;margin-bottom:32px;">共 {total_cats} 个特辑类别，{total_eps} 集节目。点击搜索或筛选查找。</p>
    </div>
    <div class="search-bar reveal">
      <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input type="text" class="search-input" id="searchInput" placeholder="搜索集名、年份、关键词...">
    </div>
    <div class="search-result-count" id="searchCount"></div>
    <div class="filters reveal" id="filters">
      {filter_btns_html}
    </div>
    <div class="cat-grid" id="catGrid">
      {cat_cards_html}
    </div>
  </div>
</section>

<section id="stats">
  <div class="container">
    <div class="reveal">
      <span class="section-tag" style="display:inline-block;font-size:13px;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;">STATISTICS</span>
      <h2 class="section-title" style="font-size:clamp(26px,4vw,36px);margin-bottom:16px;">年份统计</h2>
      <p style="font-size:16px;color:var(--text-2);max-width:600px;margin-bottom:48px;">各年份节目数量分布，看看哪一年最 prolific。</p>
    </div>
    <div class="year-stats">
      <div class="reveal">
        <div class="year-bars">
          {year_bars_html}
        </div>
      </div>
      <div class="reveal">
        <div class="year-info-card">
          <h3>年份详情</h3>
          <div class="year-info-list">
            {''.join(f'<div class="year-info-item"><span class="year-info-year">{html.escape(y)}</span><span class="year-info-eps">{year_stats[y]} 集</span></div>' for y in sorted(year_stats.keys()))}
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="members">
  <div class="container">
    <div class="reveal">
      <span class="section-tag" style="display:inline-block;font-size:13px;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;">MEMBERS</span>
      <h2 class="section-title" style="font-size:clamp(26px,4vw,36px);margin-bottom:16px;">成员变动</h2>
      <p style="font-size:16px;color:var(--text-2);max-width:600px;margin-bottom:48px;">从 2005 年首播到 2018 年停播，成员阵容经历了多次变化。</p>
    </div>
    <div class="member-tl-grid">
      <div class="reveal">
        <h3 style="font-size:18px;margin-bottom:20px;">加入与退出事件</h3>
        <div class="member-events">
          {timeline_events_html}
        </div>
      </div>
      <div class="reveal">
        <h3 style="font-size:18px;margin-bottom:20px;">成员时期</h3>
        <div class="period-list">
          {timeline_periods_html}
        </div>
      </div>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <p class="footer-text">无限挑战观看目录 | {total_eps} 集 | {total_cats} 个分类 | 2005-2018</p>
    <p class="footer-text" style="font-size:12px;">数据来源于个人观看整理，仅供参考</p>
  </div>
</footer>

<script>
// Theme switch
(function(){{
  const html=document.documentElement,btns=document.querySelectorAll('.theme-btn'),KEY='wutz-theme';
  const saved=localStorage.getItem(KEY);
  if(saved){{setTheme(saved);}}
  function setTheme(t){{
    document.body.classList.add('theme-transitioning');
    html.setAttribute('data-theme',t);
    localStorage.setItem(KEY,t);
    btns.forEach(b=>b.classList.toggle('active',b.dataset.theme===t));
    setTimeout(()=>document.body.classList.remove('theme-transitioning'),500);
  }}
  btns.forEach(b=>b.addEventListener('click',()=>setTheme(b.dataset.theme)));
}})();

// Mobile nav
(function(){{
  const t=document.getElementById('navToggle'),l=document.getElementById('navLinks');
  t.addEventListener('click',()=>{{const o=l.classList.toggle('open');t.classList.toggle('open',o);t.setAttribute('aria-expanded',o);}});
  l.querySelectorAll('.nav-link').forEach(a=>a.addEventListener('click',()=>{{l.classList.remove('open');t.classList.remove('open');t.setAttribute('aria-expanded','false');}}));
}})();

// Nav highlight
(function(){{
  const secs=document.querySelectorAll('section[id]'),links=document.querySelectorAll('.nav-link');
  const obs=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting){{const id=e.target.id;links.forEach(l=>l.classList.toggle('active',l.getAttribute('href')==='#'+id));}}}}),{{rootMargin:'-40% 0px -55% 0px'}});
  secs.forEach(s=>obs.observe(s));
}})();

// Reveal
(function(){{
  const els=document.querySelectorAll('.reveal');
  const obs=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('visible');obs.unobserve(e.target);}}}}),{{threshold:0.1,rootMargin:'0px 0px -50px 0px'}});
  els.forEach(e=>obs.observe(e));
}})();

// Year bar animation
(function(){{
  const bars=document.querySelectorAll('.year-bar-fill');
  const obs=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting){{e.target.style.width=e.target.dataset.width+'%';obs.unobserve(e.target);}}}}),{{threshold:0.3}});
  bars.forEach(b=>obs.observe(b));
}})();

// Filter
(function(){{
  const btns=document.querySelectorAll('.filter-btn'),cards=document.querySelectorAll('.cat-card');
  btns.forEach(b=>b.addEventListener('click',()=>{{
    const f=b.dataset.filter;
    btns.forEach(x=>x.classList.remove('active'));b.classList.add('active');
    cards.forEach(c=>{{c.style.display=(f==='all'||c.dataset.cat===f)?'':'none';}});
  }}));
}})();

// Search
(function(){{
  const input=document.getElementById('searchInput'),count=document.getElementById('searchCount'),cards=document.querySelectorAll('.cat-card');
  input.addEventListener('input',()=>{{
    const q=input.value.trim().toLowerCase();
    let total=0;
    cards.forEach(card=>{{
      let cardHasVisible=false;
      card.querySelectorAll('.ep-item').forEach(ep=>{{
        const t=ep.dataset.title||'';
        const match=!q||t.includes(q);
        ep.classList.toggle('hidden',!match);
        if(match){{cardHasVisible=true;total++;}}
      }});
      // Also check year tags
      card.querySelectorAll('.ep-year-tag').forEach(tag=>{{
        if(q&&tag.textContent.toLowerCase().includes(q)){{cardHasVisible=true;}}
      }});
      card.style.display=cardHasVisible?'':'none';
    }});
    count.textContent=q?`找到 ${{total}} 集匹配 "${{input.value}}"`:'';
  }});
}})();

// Category body toggle
(function(){{
  document.querySelectorAll('.cat-header').forEach(h=>{{
    h.addEventListener('click',()=>{{const b=h.nextElementSibling;b.classList.toggle('collapsed');}});
  }});
}})();
</script>
</body>
</html>'''

    output_path = r'C:\Users\hkb\.qianfan\workspace\a4256da5e8944f22b58659270dd2e291\wutz-catalog.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f'Website generated: {output_path}')
    print(f'File size: {len(full_html)} bytes')

if __name__ == '__main__':
    main()

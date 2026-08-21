#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务1：全局文字替换（精确匹配"无限挑战观看目录"）
任务2：重组index.html的卡片区域
"""
import os
import shutil
import re
from datetime import datetime

BASE_DIR = r"C:\Users\hkb\.qianfan\workspace\a4256da5e8944f22b58659270dd2e291\我的网站"

# ===== Step 1: Backup =====
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
files_to_process = [
    "index.html",
    "wutz-catalog.html",
    "timeline.html",
    "statistics.html",
    "other-watching.html"
]

print("=" * 60)
print("Step 1: Creating backups...")
for fname in files_to_process:
    src = os.path.join(BASE_DIR, fname)
    if os.path.exists(src):
        backup_name = f"{fname}.{timestamp}.bak"
        dst = os.path.join(BASE_DIR, backup_name)
        shutil.copy2(src, dst)
        print(f"  Backup: {fname} -> {backup_name}")
    else:
        print(f"  [SKIP] Not found: {fname}")

# ===== Step 2: Global text replacement =====
print("\n" + "=" * 60)
print('Step 2: Replacing "无限挑战观看目录" with "个人制作的无限挑战大览"...')

replacement_count = {}
for fname in files_to_process:
    fpath = os.path.join(BASE_DIR, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    # Exact match replacement
    new_content = content.replace("无限挑战观看目录", "个人制作的无限挑战大览")
    count = (len(content) - len(new_content)) // (len("无限挑战观看目录") - len("个人制作的无限挑战大览"))
    # Actually count occurrences properly
    count = content.count("无限挑战观看目录")
    if count > 0:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
        replacement_count[fname] = count
        print(f"  {fname}: {count} replacement(s) made")
    else:
        print(f"  {fname}: no matches found")

# ===== Step 3: Rebuild index.html cards =====
print("\n" + "=" * 60)
print("Step 3: Rebuilding index.html card section...")

index_path = os.path.join(BASE_DIR, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index_content = f.read()

# Find the projects-grid section and replace it
old_grid_start = index_content.find('<div class="projects-grid">')
old_grid_end = index_content.find('</div>\n  </div>\n</section>\n\n<section id="about">')

if old_grid_start == -1 or old_grid_end == -1:
    print("  [ERROR] Could not locate projects-grid section in index.html")
else:
    # Extract everything before and after the grid
    before = index_content[:old_grid_start]
    after = index_content[old_grid_end:]
    
    # Build new 3-card grid with modal
    new_grid = '''<div class="projects-grid">
      <!-- 个人制作的无限挑战大览 - 含弹出选择框 -->
      <div class="project-card reveal" style="text-decoration:none;color:inherit;cursor:pointer;" onclick="openWutzChoice()">
        <div class="project-cover">
          <svg viewBox="0 0 340 200" preserveAspectRatio="xMidYMid slice">
            <defs><linearGradient id="wutzGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="var(--accent)" stop-opacity="0.3"/><stop offset="100%" stop-color="var(--accent)" stop-opacity="0.05"/></linearGradient></defs>
            <rect width="340" height="200" fill="url(#wutzGrad)"/>
            <circle cx="170" cy="100" r="60" fill="none" stroke="var(--accent)" stroke-width="2" opacity="0.3"/>
            <circle cx="170" cy="100" r="40" fill="var(--accent)" opacity="0.15"/>
            <text x="170" y="95" text-anchor="middle" font-size="28" font-weight="800" fill="var(--accent)" font-family="var(--font-h)" opacity="0.6">MUCHE</text>
            <text x="170" y="120" text-anchor="middle" font-size="14" fill="var(--accent)" opacity="0.4">DOJEON</text>
            <rect x="20" y="170" width="50" height="3" rx="1.5" fill="var(--accent)" opacity="0.3"/>
            <rect x="80" y="170" width="30" height="3" rx="1.5" fill="var(--accent)" opacity="0.2"/>
            <rect x="270" y="170" width="50" height="3" rx="1.5" fill="var(--accent)" opacity="0.3"/>
          </svg>
          <span class="project-badge active">4合1入口</span>
        </div>
        <div class="project-body">
          <h3 class="project-title">个人制作的无限挑战大览</h3>
          <p class="project-desc">韩国 MBC 综艺《无限挑战》的完整观看索引与数据可视化中心。包含622集完整目录、17次成员变迁时间轴、12年3D数据统计，以及多主题切换体验。点击选择你想查看的内容。</p>
          <div class="project-stats">
            <div class="project-stat"><span class="project-stat-val">622</span><span class="project-stat-label">集数</span></div>
            <div class="project-stat"><span class="project-stat-val">39</span><span class="project-stat-label">分类</span></div>
            <div class="project-stat"><span class="project-stat-val">4项</span><span class="project-stat-label">功能</span></div>
          </div>
          <span class="project-link">点击进入选择 <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
        </div>
      </div>

      <!-- 无限挑战Logo -->
      <div class="project-card reveal" style="text-decoration:none;color:inherit;">
        <div class="project-cover" style="display:flex;align-items:center;justify-content:center;background:var(--bg-3);">
          <img src="wutz-logo.jpg" alt="无限挑战节目标志" style="width:100%;height:100%;object-fit:cover;object-position:center;" loading="lazy">
          <span class="project-badge template">Logo</span>
        </div>
        <div class="project-body">
          <h3 class="project-title">无限挑战</h3>
          <p class="project-desc">韩国MBC综艺《无限挑战》的节目标志，韩语原名为무도전 무한도전。</p>
          <div class="project-stats">
            <div class="project-stat"><span class="project-stat-val">MBC</span><span class="project-stat-label">电视台</span></div>
            <div class="project-stat"><span class="project-stat-val">2005-18</span><span class="project-stat-label">播出</span></div>
            <div class="project-stat"><span class="project-stat-val">563期</span><span class="project-stat-label">正片</span></div>
          </div>
          <span class="project-link" style="color:var(--text-3);">节目标识</span>
        </div>
      </div>

      <!-- 其他观看记录 -->
      <a href="other-watching.html" class="project-card reveal" style="text-decoration:none;color:inherit;">
        <div class="project-cover">
          <svg viewBox="0 0 340 200" preserveAspectRatio="xMidYMid slice">
            <defs><linearGradient id="otherGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="var(--accent)" stop-opacity="0.2"/><stop offset="100%" stop-color="var(--accent)" stop-opacity="0.03"/></linearGradient></defs>
            <rect width="340" height="200" fill="url(#otherGrad)"/>
            <rect x="60" y="50" width="60" height="80" rx="8" fill="var(--accent)" opacity="0.15"/>
            <rect x="140" y="40" width="60" height="90" rx="8" fill="var(--accent)" opacity="0.25"/>
            <rect x="220" y="55" width="60" height="75" rx="8" fill="var(--accent)" opacity="0.1"/>
            <polygon points="170,75 185,100 155,100" fill="var(--accent)" opacity="0.5"/>
            <rect x="30" y="160" width="280" height="2" fill="var(--accent)" opacity="0.1"/>
          </svg>
          <span class="project-badge template">模板页</span>
        </div>
        <div class="project-body">
          <h3 class="project-title">其他观看记录</h3>
          <p class="project-desc">综艺、电视剧、电影、纪录片的观看记录。提供分类管理和搜索功能，持续更新中。</p>
          <div class="project-stats">
            <div class="project-stat"><span class="project-stat-val">待填</span><span class="project-stat-label">集数</span></div>
            <div class="project-stat"><span class="project-stat-val">4</span><span class="project-stat-label">分类</span></div>
            <div class="project-stat"><span class="project-stat-val">模板</span><span class="project-stat-label">状态</span></div>
          </div>
          <span class="project-link">进入模板 <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
        </div>
      </a>
    </div>'''
    
    index_content = before + new_grid + after
    
    # Add modal HTML and JS before </body>
    modal_html = '''
<!-- WUTZ Choice Modal -->
<div class="modal-overlay" id="wutzChoiceOverlay" onclick="if(event.target===this)closeWutzChoice()"></div>
<div class="modal-box" id="wutzChoiceBox">
  <div class="modal-header">
    <span class="modal-title">个人制作的无限挑战大览</span>
    <button class="modal-close" onclick="closeWutzChoice()">&times;</button>
  </div>
  <div class="modal-body" style="padding:24px;">
    <p style="color:var(--text-2);margin-bottom:20px;font-size:14px;">选择你想查看的内容：</p>
    <div class="stats-choice-actions">
      <a href="wutz-catalog.html" class="stats-choice-btn">
        <span class="stats-choice-icon stats-choice-icon-2d"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg></span>
        <span class="stats-choice-btn-text"><span class="stats-choice-btn-label">完整目录</span><span class="stats-choice-btn-desc">622集节目按特辑分类和年份索引</span></span>
        <span class="stats-choice-arrow"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg></span>
      </a>
      <a href="timeline.html" class="stats-choice-btn">
        <span class="stats-choice-icon stats-choice-icon-2d" style="background:rgba(168,85,247,0.1);color:#a855f7;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></span>
        <span class="stats-choice-btn-text"><span class="stats-choice-btn-label">成员变动</span><span class="stats-choice-btn-desc">17次人员变动，16个时期阶段全记录</span></span>
        <span class="stats-choice-arrow"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg></span>
      </a>
      <a href="timeline.html" class="stats-choice-btn">
        <span class="stats-choice-icon stats-choice-icon-2d" style="background:rgba(39,174,96,0.1);color:#27ae60;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg></span>
        <span class="stats-choice-btn-text"><span class="stats-choice-btn-label">时间轴</span><span class="stats-choice-btn-desc">交替时间线可视化成员变迁历程</span></span>
        <span class="stats-choice-arrow"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg></span>
      </a>
      <a href="statistics.html" class="stats-choice-btn">
        <span class="stats-choice-icon stats-choice-icon-3d"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.21 15.89A10 10 0 118 2.83"/><path d="M22 12A10 10 0 0012 2v10z"/></svg></span>
        <span class="stats-choice-btn-text"><span class="stats-choice-btn-label">3D统计</span><span class="stats-choice-btn-desc">5个三维交互图表全方位解析节目数据</span></span>
        <span class="stats-choice-arrow"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg></span>
      </a>
    </div>
  </div>
</div>
<style>
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.35);z-index:300;opacity:0;pointer-events:none;transition:opacity .3s ease;backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);}
.modal-overlay.open{opacity:1;pointer-events:auto;}
.modal-box{position:fixed;top:50%;left:50%;transform:translate(-50%,-40%) scale(0.95);width:90%;max-width:520px;max-height:85vh;background:var(--card-bg);border:1px solid var(--card-border);border-radius:var(--radius-lg);box-shadow:var(--shadow-hover);z-index:301;opacity:0;pointer-events:none;transition:all .35s cubic-bezier(0.22,1,0.36,1);display:flex;flex-direction:column;overflow:hidden;}
.modal-box.open{opacity:1;pointer-events:auto;transform:translate(-50%,-50%) scale(1);}
.modal-header{display:flex;align-items:center;justify-content:space-between;padding:18px 24px;border-bottom:1px solid var(--border);flex-shrink:0;}
.modal-title{font-size:17px;font-weight:700;color:var(--text);}
.modal-close{width:32px;height:32px;border-radius:50%;border:none;background:var(--bg-3);color:var(--text-2);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:20px;transition:all .2s ease;}
.modal-close:hover{background:var(--accent-soft);color:var(--accent);transform:rotate(90deg);}
.stats-choice-actions{display:flex;flex-direction:column;gap:12px;}
.stats-choice-btn{display:flex;align-items:center;gap:12px;padding:16px 20px;border-radius:var(--radius-md);border:2px solid var(--border);background:var(--bg-2);cursor:pointer;transition:all var(--transition-fast);text-decoration:none;color:var(--text);text-align:left;}
.stats-choice-btn:hover{border-color:var(--accent);background:var(--accent-soft);transform:translateY(-2px);box-shadow:var(--shadow-hover);}
.stats-choice-icon{width:48px;height:48px;border-radius:var(--radius-sm);display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.stats-choice-icon-2d{background:rgba(59,130,246,0.1);color:#3b82f6;}
.stats-choice-icon-3d{background:rgba(217,119,6,0.1);color:#d97706;}
.stats-choice-btn-text{flex:1;}
.stats-choice-btn-label{font-size:15px;font-weight:600;color:var(--text);display:block;}
.stats-choice-btn-desc{font-size:12px;color:var(--text-2);display:block;margin-top:2px;}
.stats-choice-arrow{color:var(--text-3);transition:color var(--transition-fast),transform var(--transition-fast);}
.stats-choice-btn:hover .stats-choice-arrow{color:var(--accent);transform:translateX(4px);}
@media(max-width:480px){.modal-box{width:95%;max-height:90vh;border-radius:var(--radius-md);}.modal-header{padding:14px 18px;}.modal-body{padding:14px 18px;}.stats-choice-btn{padding:14px 16px;}.stats-choice-icon{width:40px;height:40px;}}
</style>
<script>
function openWutzChoice(){document.getElementById('wutzChoiceOverlay').classList.add('open');document.getElementById('wutzChoiceBox').classList.add('open');}
function closeWutzChoice(){document.getElementById('wutzChoiceOverlay').classList.remove('open');document.getElementById('wutzChoiceBox').classList.remove('open');}
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeWutzChoice();});
</script>'''
    
    # Insert modal before </body></html>
    body_end = index_content.rfind('</body>')
    if body_end != -1:
        index_content = index_content[:body_end] + modal_html + '\n' + index_content[body_end:]
    
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)
    print("  index.html cards rebuilt successfully (3 cards + modal)")

print("\n" + "=" * 60)
print("All tasks completed!")
print(f"Backups saved with suffix: .{timestamp}.bak")

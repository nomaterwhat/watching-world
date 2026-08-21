#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel → wutz_data.js 转换脚本
用法: python excel_to_wutz.py <输入Excel路径> [输出目录]

Excel 格式要求：
- Sheet1: 主目录数据
  - 列: 分类名 | 年份 | 标题 | [可选: 成员/备注]
- Sheet2(可选): 成员时间线
  - 列: 时期名称 | 开始年份 | 结束年份 | 成员列表
"""

import sys
import os
import json
import re
import csv

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def parse_year(text):
    """从文本中提取年份"""
    if not text or pd.isna(text) if HAS_PANDAS else not text:
        return None
    text = str(text).strip()
    # 匹配 2005年、2005、E123 250101 格式
    patterns = [
        r'(\d{4})\s*年',
        r'^(\d{4})$',
        r'E\d+\s+(\d{2})(\d{2})(\d{2})',  # E123 250101 → 2025年
        r'(\d{2})(\d{2})(\d{2})\s',  # 250101 格式
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            groups = m.groups()
            if len(groups) == 1:
                return groups[0] + '年'
            elif len(groups) == 3:
                yy = groups[0]
                year_prefix = '20' if int(yy) < 50 else '19'
                return year_prefix + yy + '年'
    return None

def normalize_title(text):
    """标准化标题"""
    if not text or (HAS_PANDAS and pd.isna(text)):
        return ''
    return str(text).strip()

def excel_to_json(excel_path):
    """读取 Excel 并转换为 JSON 结构"""
    if not HAS_PANDAS:
        raise RuntimeError('需要安装 pandas: pip install pandas openpyxl')

    df = pd.read_excel(excel_path, sheet_name=0)
    print(f"读取到 {len(df)} 行数据, 列: {list(df.columns)}")

    # 自动识别列名
    col_map = {}
    for col in df.columns:
        col_lower = str(col).lower().strip()
        if '分类' in col_lower or '类别' in col_lower or 'category' in col_lower:
            col_map['category'] = col
        elif '年份' in col_lower or 'year' in col_lower or '日期' in col_lower:
            col_map['year'] = col
        elif '标题' in col_lower or 'title' in col_lower or '名称' in col_lower or '节目' in col_lower:
            col_map['title'] = col
        elif '成员' in col_lower or 'member' in col_lower or '出演' in col_lower:
            col_map['members'] = col
        elif '备注' in col_lower or 'note' in col_lower or '标签' in col_lower:
            col_map['notes'] = col

    if 'category' not in col_map or 'title' not in col_map:
        print("警告: 未能自动识别'分类'和'标题'列, 将使用前3列作为 分类/年份/标题")
        cols = list(df.columns)
        col_map = {'category': cols[0]}
        if len(cols) > 1:
            col_map['year'] = cols[1]
        if len(cols) > 2:
            col_map['title'] = cols[2]
        else:
            col_map['title'] = cols[1]

    # 按分类分组
    categories = {}
    for _, row in df.iterrows():
        cat_name = str(row[col_map['category']]).strip() if col_map['category'] in df.columns else '未分类'
        title = normalize_title(row[col_map['title']]) if 'title' in col_map and col_map['title'] in df.columns else ''
        if not title:
            continue

        year = None
        if 'year' in col_map and col_map['year'] in df.columns:
            year = parse_year(row[col_map['year']])

        if cat_name not in categories:
            categories[cat_name] = []
        categories[cat_name].append({'year': year, 'title': title})

    # 拆分为左右两列 (简单按数量平分)
    cat_names = list(categories.keys())
    mid = (len(cat_names) + 1) // 2
    left_cats = [{'name': name, 'items': items} for name, items in categories.items()][:mid]
    right_cats = [{'name': name, 'items': items} for name, items in categories.items()][mid:]

    # 尝试读取成员时间线 (Sheet2)
    member_timeline = []
    try:
        df2 = pd.read_excel(excel_path, sheet_name=1)
        for _, row in df2.iterrows():
            parts = [str(v).strip() for v in row.values if pd.notna(v) and str(v).strip()]
            if parts:
                member_timeline.append(' '.join(parts))
    except Exception as e:
        print(f"Sheet2(成员时间线)读取跳过: {e}")
        # 使用默认时间线
        member_timeline = [
            "1.不同成员时期",
            "2005年04月23日 ~ 2005年10月22日 第一时期(6人) 主持: 刘在石、朴明洙、郑埻夏、Haha、卢弘喆、申正焕",
            "2005年10月29日 ~ 2007年03月31日 第二时期(5人时期)主持: 刘在石、朴明洙、郑埻夏、Haha、卢弘喆",
            "2007年04月07日 ~ 2007年11月17日 第三时期(6人时期)主持: 刘在石、朴明洙、郑埻夏、Haha、卢弘喆、吉成俊",
            "2007年11月24日 ~ 2008年03月22日 第四时期(6人男子团体)主持: 刘在石、朴明洙、郑埻夏、Haha、卢弘喆、Junjin",
            "2008年03月29日 ~ 2009年11月07日 第五时期(6人时期)主持: 刘在石、朴明洙、郑埻夏、Haha、卢弘喆、吉成俊",
            "2009年11月21日 ~ 2010年02月20日 第六时期(6人时期)主持: 刘在石、朴明洙、郑埻夏、Haha、卢弘喆、吉成俊、郑亨敦",
            "2010年02月27日 ~ 2011年01月22日 第七时期(7人时期)主持: 刘在石、朴明洙、郑埻夏、Haha、卢弘喆、吉成俊、郑亨敦、黄光熙",
            "2011年01月29日 ~ 2013年04月13日 第八时期(7人时期)主持: 刘在石、朴明洙、郑埻夏、Haha、卢弘喆、郑亨敦、黄光熙",
            "2013年04月20日 ~ 2014年11月22日 第九时期(6人时期)主持: 刘在石、朴明洙、郑埻夏、Haha、卢弘喆、郑亨敦、黄光熙",
            "2014年11月29日 ~ 2015年03月14日 第十时期(6人时期)主持: 刘在石、朴明洙、郑埻夏、Haha、卢弘喆、郑亨敦",
            "2015年03月21日 ~ 2016年04月02日 第十一时期(6人时期)主持: 刘在石、朴明洙、郑埻夏、Haha、卢弘喆、郑亨敦",
            "2016年04月09日 ~ 2018年03月31日 第十二时期(5人时期)主持: 刘在石、朴明洙、郑埻夏、Haha、卢弘喆、郑亨敦"
        ]

    data = {
        'left_categories': left_cats,
        'right_categories': right_cats,
        'member_timeline': member_timeline
    }
    return data

def json_to_js(data, output_path):
    """将 JSON 数据输出为 wutz_data.js 格式"""
    js_content = "// Auto-generated by excel_to_wutz.py\n"
    js_content += "const wutzData = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"已生成: {output_path}")

def main():
    if len(sys.argv) < 2:
        print("用法: python excel_to_wutz.py <输入Excel路径> [输出目录]")
        print("示例: python excel_to_wutz.py 无限挑战目录.xlsx .")
        sys.exit(1)

    excel_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(excel_path) or '.'

    if not os.path.exists(excel_path):
        print(f"错误: 找不到文件 {excel_path}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    # 1. 转换为 JSON
    data = excel_to_json(excel_path)

    # 2. 保存 JSON
    json_path = os.path.join(output_dir, 'wutz_data.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"已保存 JSON: {json_path}")

    # 3. 保存 JS
    js_path = os.path.join(output_dir, 'wutz_data.js')
    json_to_js(data, js_path)

    # 4. 统计信息
    total_eps = sum(len(c['items']) for c in data['left_categories'] + data['right_categories'])
    total_cats = len(data['left_categories']) + len(data['right_categories'])
    print(f"\n统计: {total_cats} 个分类, {total_eps} 集")
    print("完成!")

if __name__ == '__main__':
    main()

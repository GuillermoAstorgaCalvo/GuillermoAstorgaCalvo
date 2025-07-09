import json
import os

SVG_WIDTH = 500
BAR_HEIGHT = 32
BAR_GAP = 12
LEFT_MARGIN = 120
RIGHT_MARGIN = 40
TOP_MARGIN = 40
FONT_FAMILY = 'Fira Mono, monospace'
BAR_COLORS = [
    '#3178C6',  # TypeScript
    '#888888',  # Config
    '#AAAAAA',  # Unknown
    '#3776AB',  # Python
    '#CCCCCC',  # Docs
    '#4ECDC4',  # Extra
    '#FF6B6B',  # Extra
]

BADGE_ICONS = {
    'TypeScript': '🟦',
    'Python': '🐍',
    'Configuration': '⚙️',
    'Documentation': '📄',
    'Unknown': '❓',
}

def load_language_stats():
    with open('unified_stats.json', 'r', encoding='utf-8') as f:
        stats = json.load(f)
    lang_stats = stats.get('language_analysis', {})
    # Sort by lines descending
    sorted_langs = sorted(lang_stats.items(), key=lambda x: x[1]['lines'], reverse=True)
    return sorted_langs[:7]  # Top 7

def make_svg_bar_chart(lang_stats):
    max_lines = max([v[1]['lines'] for v in lang_stats]) if lang_stats else 1
    height = TOP_MARGIN + len(lang_stats) * (BAR_HEIGHT + BAR_GAP) + 40
    svg = [
        f'<svg width="{SVG_WIDTH}" height="{height}" viewBox="0 0 {SVG_WIDTH} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">',
        f'<style> .label {{ font-family: {FONT_FAMILY}; font-size: 16px; fill: #fff; }} .lang {{ font-family: {FONT_FAMILY}; font-size: 18px; font-weight: bold; fill: #fff; }} .percent {{ font-family: {FONT_FAMILY}; font-size: 14px; fill: #8B949E; }} .lines {{ font-family: {FONT_FAMILY}; font-size: 14px; fill: #8B949E; }} .title {{ font-family: {FONT_FAMILY}; font-size: 22px; font-weight: bold; fill: #fff; }} .bg {{ fill: #161B22; }} </style>',
        f'<rect class="bg" x="0" y="0" width="{SVG_WIDTH}" height="{height}" rx="16"/>'
    ]
    svg.append(f'<text x="{SVG_WIDTH//2}" y="28" text-anchor="middle" class="title">Language Ranking</text>')
    for i, (lang, data) in enumerate(lang_stats):
        y = TOP_MARGIN + i * (BAR_HEIGHT + BAR_GAP)
        bar_len = int((data['lines'] / max_lines) * (SVG_WIDTH - LEFT_MARGIN - RIGHT_MARGIN))
        color = BAR_COLORS[i % len(BAR_COLORS)]
        percent = data.get('percentage', 0)
        icon = BADGE_ICONS.get(lang, '💻')
        svg.append(f'<rect x="{LEFT_MARGIN}" y="{y}" width="{bar_len}" height="{BAR_HEIGHT}" rx="8" fill="{color}" />')
        svg.append(f'<text x="{LEFT_MARGIN - 12}" y="{y + BAR_HEIGHT//2 + 6}" text-anchor="end" class="lang">{icon} {lang}</text>')
        svg.append(f'<text x="{LEFT_MARGIN + bar_len + 8}" y="{y + BAR_HEIGHT//2 + 6}" class="percent">{percent:.1f}%</text>')
        svg.append(f'<text x="{SVG_WIDTH - RIGHT_MARGIN}" y="{y + BAR_HEIGHT//2 + 6}" text-anchor="end" class="lines">{data["lines"]:,} lines</text>')
    svg.append('</svg>')
    return '\n'.join(svg)

def main():
    lang_stats = load_language_stats()
    svg = make_svg_bar_chart(lang_stats)
    with open('language_ranking.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print('✅ language_ranking.svg generated!')

if __name__ == '__main__':
    main() 
#!/usr/bin/env python3
"""
Generate language ranking SVG from unified stats
"""

import json
import os
import sys
from pathlib import Path

def generate_language_svg_bar_chart(language_stats: dict, output_path: str):
    """Generate a modern SVG bar chart for language stats and save to output_path."""
    try:
        import svgwrite
        # Sort by LOC descending
        sorted_langs = sorted(language_stats.items(), key=lambda x: x[1]['lines'], reverse=True)
        max_loc = sorted_langs[0][1]['lines'] if sorted_langs else 1
        width = 500
        bar_height = 28
        height = bar_height * len(sorted_langs) + 40
        dwg = svgwrite.Drawing(output_path, size=(width, height))
        y = 30
        for lang, stats in sorted_langs:
            bar_len = int((stats['lines'] / max_loc) * (width - 180))
            dwg.add(dwg.rect(insert=(150, y-18), size=(bar_len, 20), fill='#4F8EF7', rx=6, ry=6))
            dwg.add(dwg.text(lang, insert=(10, y-4), font_size='16px', font_family='Segoe UI', fill='#222'))
            dwg.add(dwg.text(f"{stats['lines']:,} LOC", insert=(160 + bar_len, y-4), font_size='14px', font_family='Segoe UI', fill='#444'))
            y += bar_height
        dwg.add(dwg.text('Languages by Lines of Code', insert=(10, 20), font_size='18px', font_weight='bold', font_family='Segoe UI', fill='#222'))
        dwg.save()
        print(f"✅ SVG chart generated: {output_path}")
    except ImportError:
        print("⚠️ svgwrite not available, skipping SVG generation")
        # Create a simple text-based fallback
        with open(output_path.replace('.svg', '.txt'), 'w') as f:
            f.write("Language Statistics (SVG not available):\n")
            for lang, stats in sorted(language_stats.items(), key=lambda x: x[1]['lines'], reverse=True):
                f.write(f"{lang}: {stats['lines']:,} LOC\n")
    except Exception as e:
        print(f"⚠️ SVG generation failed: {e}")

def main():
    """Generate SVG from unified stats"""
    try:
        # Load unified stats from project root
        script_dir = Path(__file__).parent
        root_dir = script_dir.parent
        unified_stats_path = root_dir / 'unified_stats.json'
        
        if not unified_stats_path.exists():
            print("❌ unified_stats.json not found")
            sys.exit(1)
        
        with open(unified_stats_path, 'r', encoding='utf-8') as f:
            unified_stats = json.load(f)
        
        # Extract language analysis
        language_analysis = unified_stats.get('language_analysis', {})
        if not language_analysis:
            print("❌ No language analysis data found")
            sys.exit(1)
        
        # Generate SVG
        svg_path = root_dir / 'assets' / 'language_stats.svg'
        generate_language_svg_bar_chart(language_analysis, str(svg_path))
        
        print(f"✅ Language SVG generated successfully at {svg_path}")
        
    except Exception as e:
        print(f"❌ Error generating SVG: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
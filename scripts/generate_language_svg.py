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
        
        # Define categories to exclude (non-programming languages)
        excluded_categories = {
            # Configuration files
            'Configuration', 'YAML', 'JSON', 'TOML', 'INI', 'Properties',
            # Non-code categories
            'Unknown', 'Assets', 'Documentation', 'Image', 'Font', 'Archive', 'Binary',
            # Other non-programming languages
            'Log', 'Markdown', 'reStructuredText', 'AsciiDoc', 'BibTeX'
        }
        
        # Filter out excluded categories and any with 0 lines
        valid_langs = [
            (lang, stats) for lang, stats in language_stats.items()
            if stats.get('lines', 0) > 0 and lang not in excluded_categories
        ]
        sorted_langs = sorted(valid_langs, key=lambda x: x[1]['lines'], reverse=True)
        
        if not sorted_langs:
            print("⚠️ No valid programming language data found")
            return
        
        total_loc = sum(stats['lines'] for _, stats in sorted_langs)
        
        # Calculate chart dimensions
        width = 700  # Increased width for better spacing
        bar_height = 35
        max_bar_width = width - 250  # Space for labels and values
        height = bar_height * len(sorted_langs) + 80
        
        dwg = svgwrite.Drawing(output_path, size=(width, height))
        
        # Define gradients for better visual appeal
        # Add gradients directly to dwg.defs
        # Gradient for major languages (>50%)
        major_gradient = dwg.linearGradient(id="major_gradient", x1="0%", y1="0%", x2="100%", y2="0%")
        major_gradient.add_stop_color(offset="0%", color="#4F8EF7", opacity=1)
        major_gradient.add_stop_color(offset="100%", color="#2E5BB8", opacity=1)
        dwg.defs.add(major_gradient)
        # Gradient for medium languages (10-50%)
        medium_gradient = dwg.linearGradient(id="medium_gradient", x1="0%", y1="0%", x2="100%", y2="0%")
        medium_gradient.add_stop_color(offset="0%", color="#6BB6FF", opacity=1)
        medium_gradient.add_stop_color(offset="100%", color="#4F8EF7", opacity=1)
        dwg.defs.add(medium_gradient)
        # Gradient for minor languages (<10%)
        minor_gradient = dwg.linearGradient(id="minor_gradient", x1="0%", y1="0%", x2="100%", y2="0%")
        minor_gradient.add_stop_color(offset="0%", color="#A8D8FF", opacity=1)
        minor_gradient.add_stop_color(offset="100%", color="#6BB6FF", opacity=1)
        dwg.defs.add(minor_gradient)
        # Add background with subtle gradient
        bg_gradient = dwg.linearGradient(id="bg_gradient", x1="0%", y1="0%", x2="0%", y2="100%")
        bg_gradient.add_stop_color(offset="0%", color="#FAFBFC", opacity=1)
        bg_gradient.add_stop_color(offset="100%", color="#F5F7FA", opacity=1)
        dwg.defs.add(bg_gradient)
        
        dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill="url(#bg_gradient)"))
        
        # Add title with better styling
        title_group = dwg.g()
        title_group.add(dwg.text('💻 Top Programming Languages', 
                                insert=(15, 30), 
                                font_size='22px', 
                                font_weight='bold', 
                                font_family='Segoe UI, Arial, sans-serif', 
                                fill='#1A1A1A'))
        title_group.add(dwg.text('by Lines of Code', 
                                insert=(15, 50), 
                                font_size='14px', 
                                font_family='Segoe UI, Arial, sans-serif', 
                                fill='#666'))
        dwg.add(title_group)
        
        # Add total stats
        total_text = f"Total: {total_loc:,} LOC across {len(sorted_langs)} languages"
        dwg.add(dwg.text(total_text, 
                        insert=(width - 15, 25), 
                        font_size='12px', 
                        font_family='Segoe UI, Arial, sans-serif', 
                        fill='#888',
                        text_anchor="end"))
        
        y = 70
        for i, (lang, stats) in enumerate(sorted_langs):
            loc = stats.get('lines', 0)
            
            # Calculate bar width based on percentage of total (not max)
            if total_loc > 0:
                bar_ratio = loc / total_loc
                bar_width = int(bar_ratio * max_bar_width)  # Minimum 25px width
            else:
                bar_width = 0
            
            # Clamp bar width to max_bar_width
            bar_width = min(bar_width, max_bar_width)
            
            # Calculate percentage based on total LOC (not max LOC)
            percentage = (loc / total_loc) * 100 if total_loc > 0 else 0
            
            # Bar color based on percentage of total
            if percentage > 50:
                gradient_id = "major_gradient"
                rank_emoji = "🥇"
            elif percentage > 10:
                gradient_id = "medium_gradient"
                rank_emoji = "🥈"
            else:
                gradient_id = "minor_gradient"
                rank_emoji = "🥉"
            
            # Always place LOC at the far right
            loc_margin = 15
            loc_x = width - loc_margin
            # Percentage logic as before
            pct_font_size = 12
            pct_margin = 10
            pct_inside_threshold = 60  # px, bar must be at least this wide to fit percentage inside
            pct_text = f"{percentage:.1f}%"
            pct_y = y-2
            pct_fill_inside = '#fff'  # White text inside bar
            pct_fill_outside = '#4F8EF7'  # Brand color outside bar
            # Ensure bar never overlaps LOC value
            max_bar_width_adjusted = loc_x - 200 - 60  # 60px buffer for LOC and margin
            bar_width = min(bar_width, max_bar_width_adjusted)
            # Percentage placement
            if bar_width >= pct_inside_threshold:
                pct_x = 200 + bar_width - pct_margin
                pct_anchor = "end"
                pct_fill = pct_fill_inside
            else:
                pct_x = 200 + bar_width + pct_margin
                pct_anchor = "start"
                pct_fill = pct_fill_outside
            # Draw bar with shadow effect
            shadow_offset = 2
            dwg.add(dwg.rect(insert=(200 + shadow_offset, y-17 + shadow_offset), 
                            size=(bar_width, 24), 
                            fill='#000000', 
                            opacity=0.1,
                            rx=6, ry=6))
            # Main bar
            dwg.add(dwg.rect(insert=(200, y-17), 
                            size=(bar_width, 24), 
                            fill=f"url(#{gradient_id})", 
                            rx=6, ry=6))
            # Add subtle border
            dwg.add(dwg.rect(insert=(200, y-17), 
                            size=(bar_width, 24), 
                            fill='none',
                            stroke='#FFFFFF',
                            stroke_width=1,
                            opacity=0.3,
                            rx=6, ry=6))
            
            # Rank and language name
            rank_text = f"{i+1}."
            dwg.add(dwg.text(rank_text, 
                            insert=(15, y-2), 
                            font_size='12px', 
                            font_weight='bold',
                            font_family='Segoe UI, Arial, sans-serif', 
                            fill='#666'))
            
            # Language name with emoji
            lang_text = f"{rank_emoji} {lang}"
            if len(lang) > 12:
                lang_text = f"{rank_emoji} {lang[:10]}..."
            dwg.add(dwg.text(lang_text, 
                            insert=(35, y-2), 
                            font_size='14px', 
                            font_weight='bold',
                            font_family='Segoe UI, Arial, sans-serif', 
                            fill='#1A1A1A'))
            
            # LOC value at far right
            loc_text = f"{loc:,}"
            dwg.add(dwg.text(loc_text, 
                            insert=(loc_x, y-2), 
                            font_size='13px', 
                            font_weight='bold',
                            font_family='Segoe UI, Arial, sans-serif', 
                            fill='#1A1A1A',
                            text_anchor="end"))
            # "LOC" label
            dwg.add(dwg.text("LOC", 
                            insert=(loc_x, y+10), 
                            font_size='10px', 
                            font_family='Segoe UI, Arial, sans-serif', 
                            fill='#666',
                            text_anchor="end"))
            # Percentage as before
            dwg.add(dwg.text(pct_text, 
                            insert=(pct_x, pct_y),
                            font_size=f'{pct_font_size}px',
                            font_weight='bold',
                            font_family='Segoe UI, Arial, sans-serif',
                            fill=pct_fill,
                            text_anchor=pct_anchor))
            
            y += bar_height
        
        # Add footer with timestamp and stats
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
        
        # Footer background
        footer_bg = dwg.rect(insert=(0, height - 25), 
                            size=(width, 25), 
                            fill='#F8F9FA', 
                            stroke='#E9ECEF', 
                            stroke_width=1)
        dwg.add(footer_bg)
        
        # Footer text with excluded files info
        footer_text = f"📊 Generated on {timestamp} | Total: {total_loc:,} LOC | {len(sorted_langs)} languages | (excluded unnecessary files extensions like .svg, .json, .txt, .md, .log, .cfg, etc...)"
        dwg.add(dwg.text(footer_text, 
                        insert=(15, height - 8), 
                        font_size='10px', 
                        font_family='Segoe UI, Arial, sans-serif', 
                        fill='#666'))
        
        dwg.save()
        print(f"✅ SVG chart generated: {output_path}")
        print(f"📊 Chart shows {len(sorted_langs)} languages")
        print(f"📈 Max LOC: {sorted_langs[0][1]['lines']:,}, Min LOC: {sorted_langs[-1][1]['lines']:,}")
        print(f"🎨 Enhanced with gradients and professional styling")
        
    except ImportError:
        print("⚠️ svgwrite not available, skipping SVG generation")
        # Create a simple text-based fallback
        with open(output_path.replace('.svg', '.txt'), 'w') as f:
            f.write("Language Statistics (SVG not available):\n")
            for lang, stats in sorted(language_stats.items(), key=lambda x: x[1].get('lines', 0), reverse=True):
                f.write(f"{lang}: {stats.get('lines', 0):,} LOC\n")
    except Exception as e:
        print(f"⚠️ SVG generation failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Generate SVG from unified stats"""
    try:
        # Load unified stats from project root (when running from scripts directory)
        script_dir = Path(__file__).parent
        root_dir = script_dir.parent
        unified_stats_path = root_dir / 'unified_stats.json'
        
        # If not found in root, try current directory (for local testing)
        if not unified_stats_path.exists():
            unified_stats_path = Path('unified_stats.json')
        
        print(f"🔍 Looking for unified_stats.json at: {unified_stats_path}")
        print(f"📁 Current working directory: {Path.cwd()}")
        print(f"📁 Script directory: {script_dir}")
        print(f"📁 Root directory: {root_dir}")
        
        if not unified_stats_path.exists():
            print("❌ unified_stats.json not found")
            print("📁 Available files in root directory:")
            if root_dir.exists():
                for file in root_dir.iterdir():
                    print(f"  - {file.name}")
            sys.exit(1)
        
        with open(unified_stats_path, 'r', encoding='utf-8') as f:
            unified_stats = json.load(f)
        
        # Extract language analysis
        language_analysis = unified_stats.get('language_analysis', {})
        if not language_analysis:
            print("❌ No language analysis data found")
            sys.exit(1)
        
        # Debug: Print language data
        print(f"📊 Found {len(language_analysis)} languages in data:")
        total_loc = sum(stats.get('lines', 0) for stats in language_analysis.values())
        print(f"📈 Total LOC: {total_loc:,}")
        for lang, stats in sorted(language_analysis.items(), key=lambda x: x[1].get('lines', 0), reverse=True):
            loc = stats.get('lines', 0)
            percentage = (loc / total_loc * 100) if total_loc > 0 else 0
            print(f"  - {lang}: {loc:,} LOC ({percentage:.1f}%)")
        print(f"✅ Percentages now calculated correctly based on total LOC")
        
        # Generate SVG
        svg_path = root_dir / 'assets' / 'language_stats.svg'
        print(f"🎨 Generating SVG at: {svg_path}")
        generate_language_svg_bar_chart(language_analysis, str(svg_path))
        
        # Verify the SVG was created
        if svg_path.exists():
            print(f"✅ Language SVG generated successfully at {svg_path}")
            print(f"📏 SVG file size: {svg_path.stat().st_size} bytes")
        else:
            print(f"❌ SVG file was not created at {svg_path}")
        
    except Exception as e:
        print(f"❌ Error generating SVG: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
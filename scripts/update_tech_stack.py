#!/usr/bin/env python3
"""
Update Tech Stack Script
Updates the existing unified_stats.json to use the new tech stack format with actual technologies.
"""

import json
from pathlib import Path


def update_tech_stack_format():
    """Update the tech stack format in unified_stats.json."""
    
    # Load current stats
    stats_file = Path('unified_stats.json')
    if not stats_file.exists():
        print("❌ unified_stats.json not found")
        return
    
    with open(stats_file, 'r', encoding='utf-8') as f:
        stats = json.load(f)
    
    # Get language analysis
    language_analysis = stats.get('language_analysis', {})
    
    # Create new tech stack analysis
    tech_stack_analysis = {
        'frontend': {'technologies': [], 'total_loc': 0},
        'backend': {'technologies': [], 'total_loc': 0},
        'database': {'technologies': [], 'total_loc': 0},
        'devops': {'technologies': [], 'total_loc': 0},
        'ai_ml': {'technologies': [], 'total_loc': 0}
    }
    
    # Map languages to actual technologies
    lang_to_tech = {
        'TypeScript': 'TypeScript, React, Next.js',
        'JavaScript': 'JavaScript, Node.js',
        'Python': 'Python, FastAPI, Django',
        'HTML': 'HTML',
        'CSS': 'CSS, TailwindCSS'
    }
    
    # Process each language
    for lang, lang_stats in language_analysis.items():
        loc = lang_stats.get('lines', 0)
        
        if lang in lang_to_tech:
            tech_names = lang_to_tech[lang].split(', ')
            
            if lang in ['TypeScript', 'JavaScript', 'HTML', 'CSS']:
                tech_stack_analysis['frontend']['technologies'].extend(tech_names)
                tech_stack_analysis['frontend']['total_loc'] += loc
            elif lang == 'Python':
                tech_stack_analysis['backend']['technologies'].extend(tech_names)
                tech_stack_analysis['backend']['total_loc'] += loc
    
    # Remove duplicates and sort
    for category in tech_stack_analysis.values():
        category['technologies'] = sorted(list(set(category['technologies'])))
    
    # Update the stats
    stats['tech_stack_analysis'] = tech_stack_analysis
    
    # Save updated stats
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print("✅ Updated tech stack format in unified_stats.json")
    print("\n📊 New Tech Stack Analysis:")
    for category, data in tech_stack_analysis.items():
        if data['technologies']:
            print(f"\n{category.title()}:")
            for tech in data['technologies']:
                print(f"  • {tech}")


if __name__ == "__main__":
    update_tech_stack_format() 
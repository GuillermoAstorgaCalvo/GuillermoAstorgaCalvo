#!/usr/bin/env python3
"""
Debug Language Detection Script
Helps identify files that are being incorrectly categorized.
"""

import json
import os
import sys
from pathlib import Path
from language_mapper import get_language_mapper


def analyze_repository_languages(repo_path: str):
    """Analyze language detection for a repository."""
    repo_path = Path(repo_path)
    language_mapper = get_language_mapper()
    
    # Collect all files
    all_files = []
    for root, dirs, files in os.walk(repo_path):
        # Skip common directories to ignore
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'node_modules', 'venv', '.venv', 'build', 'dist'}]
        
        for file in files:
            # Skip .txt and .json files
            if file.endswith('.txt') or file.endswith('.json'):
                continue
            file_path = Path(root) / file
            relative_path = file_path.relative_to(repo_path)
            all_files.append(str(relative_path))
    
    # Analyze each file
    language_stats = {}
    unknown_files = []
    config_files = []
    
    for file_path in all_files:
        language = language_mapper.get_language_from_filename(file_path)
        
        if language not in language_stats:
            language_stats[language] = {
                'count': 0,
                'files': []
            }
        
        language_stats[language]['count'] += 1
        language_stats[language]['files'].append(file_path)
        
        # Track potentially problematic categorizations
        if language == 'Unknown':
            unknown_files.append(file_path)
        elif language in ['Configuration', 'YAML', 'JSON', 'TOML', 'INI', 'Properties']:
            config_files.append((file_path, language))
        elif file_path.endswith('.txt'):
            # .txt files are mostly logs and should be ignored
            pass
    
    # Print analysis
    print(f"🔍 Language Detection Analysis for: {repo_path}")
    print(f"📁 Total files found: {len(all_files)}")
    print()
    
    # Show language breakdown
    print("📊 Language Breakdown:")
    for lang, stats in sorted(language_stats.items(), key=lambda x: x[1]['count'], reverse=True):
        print(f"  {lang}: {stats['count']} files")
        if stats['count'] <= 5:  # Show details for small categories
            for file in stats['files']:
                print(f"    - {file}")
        print()
    
    # Show unknown files
    if unknown_files:
        print("❓ Unknown Files (need investigation):")
        for file in sorted(unknown_files):
            print(f"  - {file}")
        print()
    
    # Show config files
    if config_files:
        print("⚙️ Configuration Files (check if correctly categorized):")
        for file, lang in sorted(config_files):
            print(f"  - {file} → {lang}")
        print()
    
    return language_stats


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python debug_language_detection.py <repository_path>")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    if not os.path.exists(repo_path):
        print(f"❌ Repository path does not exist: {repo_path}")
        sys.exit(1)
    
    analyze_repository_languages(repo_path)


if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Repository Statistics Processing Script
Processes git fame statistics for a single repository and saves results.
"""

import json
import sys
import os
from pathlib import Path
import subprocess

# Add scripts directory to Python path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from config_manager import get_config_manager
from git_fame_parser import GitFameParser
from stats_processor import StatsProcessor, AuthorMatcher
from language_mapper import get_language_mapper


def run_cloc_on_repo(repo_path: Path) -> dict:
    """Run cloc on the given repo path and return the parsed JSON output."""
    try:
        # Focus on real code languages, exclude configuration files
        result = subprocess.run([
            'cloc', '--json', '--quiet', '--timeout=60',
            '--include-lang=Python,TypeScript,JavaScript,HTML,CSS,Shell',
            '--exclude-dir=.git,node_modules,venv,build,dist,data,output,logs,generated,target,coverage,.nyc_output',
            '--exclude-ext=json,toml,lock,yml,yaml,ini,cfg,conf,env,log,md,txt,svg,png,jpg,jpeg,gif,ico,bmp,tiff,webp',
            str(repo_path)
        ], capture_output=True, text=True, timeout=120, check=True)
        cloc_output = result.stdout
        cloc_data = json.loads(cloc_output)
        return cloc_data
    except Exception as e:
        print(f"⚠️ cloc failed: {e}")
        return {}


def generate_language_svg_bar_chart(language_stats: dict, output_path: str):
    """Generate a modern SVG bar chart for language stats and save to output_path."""
    try:
        import svgwrite
        # Sort by LOC descending
        sorted_langs = sorted(language_stats.items(), key=lambda x: x[1]['loc'], reverse=True)
        max_loc = sorted_langs[0][1]['loc'] if sorted_langs else 1
        width = 500
        bar_height = 28
        height = bar_height * len(sorted_langs) + 40
        dwg = svgwrite.Drawing(output_path, size=(width, height))
        y = 30
        for lang, stats in sorted_langs:
            bar_len = int((stats['loc'] / max_loc) * (width - 180))
            dwg.add(dwg.rect(insert=(150, y-18), size=(bar_len, 20), fill='#4F8EF7', rx=6, ry=6))
            dwg.add(dwg.text(lang, insert=(10, y-4), font_size='16px', font_family='Segoe UI', fill='#222'))
            dwg.add(dwg.text(f"{stats['loc']:,} LOC", insert=(160 + bar_len, y-4), font_size='14px', font_family='Segoe UI', fill='#444'))
            y += bar_height
        dwg.add(dwg.text('Languages by Lines of Code', insert=(10, 20), font_size='18px', font_weight='bold', font_family='Segoe UI', fill='#222'))
        dwg.save()
        print(f"✅ SVG chart generated: {output_path}")
    except ImportError:
        print("⚠️ svgwrite not available, skipping SVG generation")
        # Create a simple text-based fallback
        with open(output_path.replace('.svg', '.txt'), 'w') as f:
            f.write("Language Statistics (SVG not available):\n")
            for lang, stats in sorted(language_stats.items(), key=lambda x: x[1]['loc'], reverse=True):
                f.write(f"{lang}: {stats['loc']:,} LOC\n")
    except Exception as e:
        print(f"⚠️ SVG generation failed: {e}")


def main():
    language_stats = {}  # Ensure language_stats is always defined
    try:
        # Load configuration
        config = get_config_manager()
        
        # Validate configuration
        config_errors = config.validate_config()
        if config_errors:
            print("❌ Configuration validation failed:")
            for error in config_errors:
                print(f"   - {error}")
            sys.exit(1)
        
        # Get repository information from environment or command line
        repo_name = os.environ.get('REPO_NAME')
        display_name = os.environ.get('DISPLAY_NAME')
        
        if not repo_name:
            print("❌ Error: REPO_NAME environment variable not set")
            sys.exit(1)
        
        if not display_name:
            # Try to get display name from config
            repo_config = config.get_repository_by_name(repo_name)
            if repo_config:
                display_name = repo_config.get('display_name', repo_name)
            else:
                display_name = repo_name
        
        # Initialize components
        git_fame_parser = GitFameParser(timeout_seconds=config.get_timeout_seconds())
        author_matcher = AuthorMatcher(
            guillermo_patterns=config.get_guillermo_patterns(),
            bot_patterns=config.get_bot_patterns()
        )
        stats_processor = StatsProcessor(author_matcher)
        language_mapper = get_language_mapper()
        
        # Process repository
        print(f"Processing repository: {display_name}")
        
        # Execute git fame and parse data
        # Repository is cloned to parent directory (root), not in scripts/
        repo_path = script_dir.parent / "repo"
        print(f"Looking for repository at: {repo_path}")
        
        if not repo_path.exists():
            print(f"❌ Repository directory not found at: {repo_path}")
            print(f"Current working directory: {Path.cwd()}")
            print(f"Available files in parent directory:")
            parent_dir = script_dir.parent
            if parent_dir.exists():
                for item in parent_dir.iterdir():
                    print(f"  - {item.name}")
            sys.exit(1)
        
        # Run cloc for accurate language stats (with timeout)
        print("🔍 Running cloc for accurate language stats...")
        try:
            cloc_data = run_cloc_on_repo(repo_path)
            cloc_language_stats = {}
            if cloc_data:
                for lang, stats in cloc_data.items():
                    # Exclude configuration and non-code languages
                    if lang in ('header', 'SUM', 'JSON', 'Text', 'YAML', 'TOML', 'INI', 'Markdown', 'Properties', 'Image', 'SVG'):
                        continue
                    cloc_language_stats[lang] = {
                        'loc': stats.get('code', 0),
                        'files': stats.get('nFiles', 0),
                        'commits': 0  # cloc doesn't provide commits
                    }
                print(f"✅ cloc found {len(cloc_language_stats)} languages")
            else:
                print("⚠️ cloc did not return any language stats")
        except Exception as e:
            print(f"⚠️ cloc failed, using fallback: {e}")
            cloc_language_stats = {}

        # Get regular git fame data (by author) - this provides REAL commit data
        git_fame_data = git_fame_parser.execute_git_fame(
            str(repo_path), 
            config.get_git_fame_format()
        )
        
        if not git_fame_data:
            print("❌ Failed to get git fame data")
            sys.exit(1)
        
        # Validate git fame data
        if not git_fame_parser.validate_git_fame_data(git_fame_data):
            print("❌ Invalid git fame data format")
            sys.exit(1)
        
        # Extract author information - this contains REAL commit and file counts
        authors = git_fame_parser.extract_authors(git_fame_data)
        
        if not authors:
            print("❌ No author data found")
            sys.exit(1)
        
        # Get language breakdown data (for LOC only, commits/files will be distributed proportionally)
        print("📊 Getting language breakdown...")
        git_fame_bytype_data = git_fame_parser.execute_git_fame(
            str(repo_path),
            config.get_git_fame_format(),
            by_type=True
        )
        
        language_stats = {}
        if git_fame_bytype_data:
            # Extract extension stats (LOC only, no estimated commits/files)
            extension_stats = git_fame_parser.extract_extension_stats(git_fame_bytype_data)
            print(f"📊 Extracted {len(extension_stats)} file extensions")
            
            # Convert to language stats
            language_stats = language_mapper.get_language_stats(extension_stats)
            print(f"✅ Found {len(language_stats)} languages")
            
            # Debug: Show detailed language breakdown
            if language_stats:
                sorted_langs = sorted(language_stats.items(), key=lambda x: x[1]['loc'], reverse=True)
                print("🏆 Language breakdown:")
                for lang, stats in sorted_langs:
                    print(f"  - {lang}: {stats['loc']:,} LOC ({stats['files']} files)")
                
                # Show problematic categorizations
                config_langs = [lang for lang, stats in sorted_langs if lang in ['Configuration', 'YAML', 'JSON', 'TOML', 'INI', 'Properties']]
                if config_langs:
                    print(f"⚠️ Configuration-like languages found: {', '.join(config_langs)}")
                
                unknown_langs = [lang for lang, stats in sorted_langs if lang == 'Unknown']
                if unknown_langs:
                    print(f"❓ Unknown languages found: {len(unknown_langs)} files")
                
                # Note about .txt files being excluded
                print("ℹ️ Note: .txt files are excluded as they are mostly logs")
            else:
                print("⚠️ No language stats generated")
        else:
            print("⚠️ Could not get language breakdown data")
            print("🔍 Debug: git fame --bytype output was empty or failed")
        
        # Process repository statistics using REAL author data
        repo_stats = stats_processor.process_repository_data(authors, display_name)
        repo_stats.language_stats = language_stats
        
        # Convert to dictionary for JSON serialization
        stats_dict = repo_stats.to_dict()
        
        # Save results to JSON file in scripts directory
        output_filename = config.get_stats_filename()
        output_path = script_dir / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats_dict, f, indent=2, ensure_ascii=False)
        
        print("✅ Repository statistics processed successfully!")
        
        # Print summary for debugging (optional)
        guillermo_stats = repo_stats.guillermo_stats
        repo_totals = repo_stats.repo_totals
        
        if repo_totals.loc > 0:
            loc_pct = (guillermo_stats.loc / repo_totals.loc) * 100
            print(f"📊 Summary: {guillermo_stats.loc:,} LOC ({loc_pct:.1f}%), "
                  f"{guillermo_stats.commits} commits, {guillermo_stats.files} files")
        
        # After language stats aggregation:
        # generate_language_svg_bar_chart(cloc_language_stats, 'assets/language_stats.svg')
        # Note: SVG generation moved to aggregation job
        
        # After processing repo stats, run dependency analyzer for this repo
        from dependency_analyzer import DependencyAnalyzer
        repo_dir = script_dir.parent / "repo"
        analyzer = DependencyAnalyzer()
        print(f"[DEBUG] (process_repo_stats.py) Analyzing dependencies in: {repo_dir}")
        tech_stack = analyzer.analyze_repository_dependencies(repo_dir)
        # Convert sets to the format expected by aggregation script
        tech_stack_serializable = {}
        for category, techs in tech_stack.items():
            tech_list = sorted(list(techs))
            tech_stack_serializable[category] = {
                'technologies': tech_list,
                'count': len(tech_list)
            }
        with open('tech_stack_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(tech_stack_serializable, f, indent=2, ensure_ascii=False)
        print(f"[DEBUG] (process_repo_stats.py) Saved tech_stack_analysis.json for {repo_dir}")
        
    except KeyboardInterrupt:
        print("\n❌ Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
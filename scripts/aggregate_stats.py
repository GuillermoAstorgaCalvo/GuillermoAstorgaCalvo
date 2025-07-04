#!/usr/bin/env python3
"""
Statistics Aggregation Script
Aggregates statistics from multiple repositories and generates unified reports.
"""

import json
import sys
from pathlib import Path
from typing import List

# Add scripts directory to Python path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from config_manager import get_config_manager
from stats_processor import StatsProcessor, AuthorMatcher, RepositoryStats, AuthorStats
from report_generator import MarkdownReportGenerator, JSONReportGenerator
from language_mapper import get_language_mapper


def load_repository_stats(stats_dir: str = None) -> List[RepositoryStats]:
    """
    Load repository statistics from artifact files.
    
    Args:
        stats_dir: Directory containing repository statistics artifacts
        
    Returns:
        List of RepositoryStats objects
    """
    stats_data = []
    
    # Default to parent directory where artifacts are downloaded
    if stats_dir is None:
        stats_dir = script_dir.parent / "repo-stats"
    else:
        stats_dir = Path(stats_dir)
    
    print(f"Looking for statistics in: {stats_dir}")
    
    if not stats_dir.exists():
        print(f"❌ Statistics directory not found: {stats_dir}")
        print(f"Current working directory: {Path.cwd()}")
        print(f"Available files in parent directory:")
        parent_dir = script_dir.parent
        if parent_dir.exists():
            for item in parent_dir.iterdir():
                print(f"  - {item.name}")
        return []
    
    # Process each artifact directory
    for artifact_dir in stats_dir.iterdir():
        if artifact_dir.is_dir():
            stats_file = artifact_dir / 'repo_stats.json'
            if stats_file.exists():
                try:
                    with open(stats_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Convert dictionary back to RepositoryStats object
                    language_stats = data.get('language_stats', {})
                    print(f"📊 Loading language stats for {data['display_name']}: {len(language_stats)} languages")
                    
                    repo_stats = RepositoryStats(
                        display_name=data['display_name'],
                        guillermo_stats=AuthorStats(**data['guillermo_stats']),
                        repo_totals=AuthorStats(**data['repo_totals']),
                        language_stats=language_stats
                    )
                    
                    stats_data.append(repo_stats)
                    print(f"✅ Loaded statistics for: {data['display_name']}")
                    
                except (json.JSONDecodeError, KeyError, TypeError) as e:
                    print(f"❌ Failed to load statistics from {stats_file}: {e}")
                except Exception as e:
                    print(f"❌ Unexpected error loading {stats_file}: {e}")
    
    return stats_data


def main():
    """Main function to aggregate statistics and generate reports."""
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
        
        # Initialize components
        author_matcher = AuthorMatcher(
            guillermo_patterns=config.get_guillermo_patterns(),
            bot_patterns=config.get_bot_patterns()
        )
        stats_processor = StatsProcessor(author_matcher)
        language_mapper = get_language_mapper()
        
        # Load repository statistics from artifacts
        print("Loading repository statistics...")
        repository_stats_list = load_repository_stats()
        
        if not repository_stats_list:
            print("❌ Fatal error: Could not load any repository statistics")
            sys.exit(1)
        
        print(f"📊 Loaded statistics from {len(repository_stats_list)} repositories")
        
        # Aggregate statistics
        print("Aggregating unified statistics...")
        unified_stats = stats_processor.aggregate_repository_stats(repository_stats_list)
        
        # Debug: Check aggregated language stats
        if hasattr(unified_stats, 'unified_language_stats') and unified_stats.unified_language_stats:
            print(f"✅ Aggregated language stats: {len(unified_stats.unified_language_stats)} languages")
            for lang, stats_data in unified_stats.unified_language_stats.items():
                print(f"  - {lang}: {stats_data['loc']} LOC")
        else:
            print("⚠️ No aggregated language stats found")
        
        # Validate aggregated statistics
        validation_errors = stats_processor.validate_unified_stats(unified_stats)
        if validation_errors:
            print("❌ Statistics validation failed:")
            for error in validation_errors:
                print(f"   - {error}")
            sys.exit(1)
        
        # Generate reports
        print("Generating reports...")
        
        # Initialize report generators with configuration
        report_config = config.get_report_config()
        markdown_generator = MarkdownReportGenerator(
            title=config.get_report_title(),
            date_format=config.get_date_format()
        )
        json_generator = JSONReportGenerator()
        
        # Generate markdown report in scripts directory
        markdown_filename = config.get_report_filename()
        markdown_path = script_dir / markdown_filename
        
        # Get full config for analytics
        full_config = config.get_full_config()
        markdown_generator.save_report(unified_stats, str(markdown_path), full_config)
        print(f"✅ Markdown report saved to: {markdown_path}")
        
        # Generate JSON report in scripts directory
        json_filename = "unified_stats.json"
        json_path = script_dir / json_filename
        json_generator.save_report(unified_stats, str(json_path))
        print(f"✅ JSON report saved to: {json_path}")
        
        # Print summary
        guillermo = unified_stats.guillermo_unified
        global_totals = AuthorStats(
            loc=unified_stats.total_loc,
            commits=unified_stats.total_commits,
            files=unified_stats.total_files
        )
        
        loc_pct, commits_pct, files_pct = stats_processor.calculate_distribution_percentages(
            guillermo, global_totals
        )
        
        print("\n📈 Final Summary:")
        print(f"   Repositories processed: {unified_stats.repos_processed}")
        print(f"   Total LOC: {unified_stats.total_loc:,}")
        print(f"   Total commits: {unified_stats.total_commits:,}")
        print(f"   Total files: {unified_stats.total_files:,}")
        print(f"   Guillermo's contributions: {guillermo.loc:,} LOC ({loc_pct:.1f}%), "
              f"{guillermo.commits:,} commits ({commits_pct:.1f}%), "
              f"{guillermo.files:,} files ({files_pct:.1f}%)")
        
        print("\n✅ Statistics aggregation completed successfully!")
        
    except KeyboardInterrupt:
        print("\n❌ Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
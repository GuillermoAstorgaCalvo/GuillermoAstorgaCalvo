#!/usr/bin/env python3
"""
Repository Statistics Processing Script
Processes git fame statistics for a single repository and saves results.
"""

import json
import sys
import os
from pathlib import Path

# Add scripts directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config_manager import get_config_manager
from git_fame_parser import GitFameParser
from stats_processor import StatsProcessor, AuthorMatcher


def main():
    """Main function to process repository statistics."""
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
        
        # Process repository
        print(f"Processing repository: {display_name}")
        
        # Execute git fame and parse data
        repo_path = "repo"  # Default clone directory
        git_fame_data = git_fame_parser.execute_git_fame(
            repo_path, 
            config.get_git_fame_format()
        )
        
        if not git_fame_data:
            print("❌ Failed to get git fame data")
            sys.exit(1)
        
        # Validate git fame data
        if not git_fame_parser.validate_git_fame_data(git_fame_data):
            print("❌ Invalid git fame data format")
            sys.exit(1)
        
        # Extract author information
        authors = git_fame_parser.extract_authors(git_fame_data)
        
        if not authors:
            print("❌ No author data found")
            sys.exit(1)
        
        # Process repository statistics
        repo_stats = stats_processor.process_repository_data(authors, display_name)
        
        # Convert to dictionary for JSON serialization
        stats_dict = repo_stats.to_dict()
        
        # Save results to JSON file
        output_filename = config.get_stats_filename()
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(stats_dict, f, indent=2, ensure_ascii=False)
        
        print("✅ Repository statistics processed successfully!")
        
        # Print summary for debugging (optional)
        guillermo_stats = repo_stats.guillermo_stats
        repo_totals = repo_stats.repo_totals
        
        if repo_totals.loc > 0:
            loc_pct = (guillermo_stats.loc / repo_totals.loc) * 100
            print(f"📊 Summary: {guillermo_stats.loc:,} LOC ({loc_pct:.1f}%), "
                  f"{guillermo_stats.commits} commits, {guillermo_stats.files} files")
        
    except KeyboardInterrupt:
        print("\n❌ Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
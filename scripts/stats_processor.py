"""
Statistics Processor Module
Handles core statistics processing logic including author matching and aggregation.
"""

import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class AuthorStats:
    """Represents statistics for a single author."""
    loc: int = 0
    commits: int = 0
    files: int = 0
    
    def add(self, other: 'AuthorStats') -> None:
        """Add another AuthorStats to this one."""
        self.loc += other.loc
        self.commits += other.commits
        self.files += other.files
    
    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary."""
        return {
            'loc': self.loc,
            'commits': self.commits,
            'files': self.files
        }


@dataclass
class RepositoryStats:
    """Represents statistics for a single repository."""
    display_name: str
    guillermo_stats: AuthorStats
    repo_totals: AuthorStats
    language_stats: Dict[str, Dict[str, int]] = None
    
    def __post_init__(self):
        if self.language_stats is None:
            self.language_stats = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'display_name': self.display_name,
            'guillermo_stats': self.guillermo_stats.to_dict(),
            'repo_totals': self.repo_totals.to_dict(),
            'language_stats': self.language_stats
        }


@dataclass
class UnifiedStats:
    """Represents unified statistics across all repositories."""
    total_commits: int = 0
    total_files: int = 0
    total_loc: int = 0
    repos_processed: int = 0
    guillermo_unified: AuthorStats = None
    repo_breakdown: Dict[str, RepositoryStats] = None
    unified_language_stats: Dict[str, Dict[str, int]] = None
    
    def __post_init__(self):
        if self.guillermo_unified is None:
            self.guillermo_unified = AuthorStats()
        if self.repo_breakdown is None:
            self.repo_breakdown = {}
        if self.unified_language_stats is None:
            self.unified_language_stats = {}


class AuthorMatcher:
    """Handles author pattern matching and classification."""
    
    def __init__(self, guillermo_patterns: List[str], bot_patterns: List[str]):
        """
        Initialize the author matcher.
        
        Args:
            guillermo_patterns: Regex patterns to match Guillermo's authorship
            bot_patterns: Regex patterns to match bot authors
        """
        self.guillermo_patterns = guillermo_patterns
        self.bot_patterns = bot_patterns
    
    def is_guillermo(self, author_name: str) -> bool:
        """
        Check if an author name matches Guillermo patterns.
        
        Args:
            author_name: Author name to check
            
        Returns:
            True if matches Guillermo patterns
        """
        return any(re.search(pattern, str(author_name), re.IGNORECASE) 
                  for pattern in self.guillermo_patterns)
    
    def is_bot(self, author_name: str) -> bool:
        """
        Check if an author name matches bot patterns.
        
        Args:
            author_name: Author name to check
            
        Returns:
            True if matches bot patterns
        """
        return any(re.search(pattern, str(author_name), re.IGNORECASE) 
                  for pattern in self.bot_patterns)
    
    def classify_author(self, author_name: str) -> str:
        """
        Classify an author as 'guillermo', 'bot', or 'other'.
        
        Args:
            author_name: Author name to classify
            
        Returns:
            Classification string
        """
        if self.is_bot(author_name):
            return 'bot'
        elif self.is_guillermo(author_name):
            return 'guillermo'
        else:
            return 'other'


class StatsProcessor:
    """Main statistics processing class."""
    
    def __init__(self, author_matcher: AuthorMatcher):
        """
        Initialize the stats processor.
        
        Args:
            author_matcher: AuthorMatcher instance for classifying authors
        """
        self.author_matcher = author_matcher
    
    def process_repository_data(self, authors: List[Tuple[str, int, int, int]], 
                              display_name: str) -> RepositoryStats:
        """
        Process author data for a single repository.
        
        Args:
            authors: List of (author_name, loc, commits, files) tuples
            display_name: Display name for the repository
            
        Returns:
            RepositoryStats object
        """
        guillermo_stats = AuthorStats()
        repo_totals = AuthorStats()
        
        for author_name, loc, commits, files in authors:
            author_classification = self.author_matcher.classify_author(author_name)
            
            # Only count human contributors (exclude bots)
            if author_classification != 'bot':
                repo_totals.loc += loc
                repo_totals.commits += commits
                repo_totals.files += files
                
                # Track Guillermo's contributions
                if author_classification == 'guillermo':
                    guillermo_stats.loc += loc
                    guillermo_stats.commits += commits
                    guillermo_stats.files += files
        
        return RepositoryStats(
            display_name=display_name,
            guillermo_stats=guillermo_stats,
            repo_totals=repo_totals
        )
    
    def aggregate_repository_stats(self, repository_stats_list: List[RepositoryStats]) -> UnifiedStats:
        """
        Aggregate statistics from multiple repositories.
        
        Args:
            repository_stats_list: List of RepositoryStats objects
            
        Returns:
            UnifiedStats object
        """
        unified_stats = UnifiedStats()
        unified_stats.repos_processed = len(repository_stats_list)
        unified_stats.guillermo_unified = AuthorStats()
        unified_stats.repo_breakdown = {}
        unified_stats.unified_language_stats = {}
        
        for repo_stats in repository_stats_list:
            # Add to unified totals
            unified_stats.total_loc += repo_stats.repo_totals.loc
            unified_stats.total_commits += repo_stats.repo_totals.commits
            unified_stats.total_files += repo_stats.repo_totals.files
            
            # Add to Guillermo's unified stats
            unified_stats.guillermo_unified.add(repo_stats.guillermo_stats)
            
            # Aggregate language stats
            for language, stats in repo_stats.language_stats.items():
                if language not in unified_stats.unified_language_stats:
                    unified_stats.unified_language_stats[language] = {
                        'loc': 0,
                        'commits': 0,
                        'files': 0
                    }
                
                unified_stats.unified_language_stats[language]['loc'] += stats.get('loc', 0)
                unified_stats.unified_language_stats[language]['commits'] += stats.get('commits', 0)
                unified_stats.unified_language_stats[language]['files'] += stats.get('files', 0)
            
            # Store individual repository breakdown
            unified_stats.repo_breakdown[repo_stats.display_name] = repo_stats
        
        return unified_stats
    
    def calculate_distribution_percentages(self, stats: AuthorStats, totals: AuthorStats) -> Tuple[float, float, float]:
        """
        Calculate distribution percentages for an author's contributions.
        
        Args:
            stats: Author's statistics
            totals: Total repository statistics
            
        Returns:
            Tuple of (loc_percentage, commits_percentage, files_percentage)
        """
        loc_pct = (stats.loc / totals.loc * 100) if totals.loc > 0 else 0
        commits_pct = (stats.commits / totals.commits * 100) if totals.commits > 0 else 0
        files_pct = (stats.files / totals.files * 100) if totals.files > 0 else 0
        
        return (loc_pct, commits_pct, files_pct)
    
    def validate_unified_stats(self, stats: UnifiedStats) -> List[str]:
        """
        Validate unified statistics and return any validation errors.
        
        Args:
            stats: UnifiedStats object to validate
            
        Returns:
            List of validation error messages
        """
        errors = []
        
        if stats.guillermo_unified.loc == 0:
            errors.append("No Guillermo contributions found")
        
        if stats.repos_processed == 0:
            errors.append("No repositories processed")
        
        if stats.total_loc == 0:
            errors.append("No lines of code found")
        
        if not stats.repo_breakdown:
            errors.append("No repository breakdown data")
        
        return errors 
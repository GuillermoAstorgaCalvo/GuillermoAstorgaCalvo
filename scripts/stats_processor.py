"""
Statistics Processor Module
Handles core statistics processing logic including author matching and aggregation.
"""

import re
from dataclasses import dataclass
from typing import Any

from error_handling import StatsProcessingError, get_logger, log_and_raise


@dataclass
class AuthorStats:
    """Represents statistics for a single author."""

    loc: int = 0
    commits: int = 0
    files: int = 0

    def add(self, other: "AuthorStats") -> None:
        """Add another AuthorStats to this one."""
        try:
            self.loc += other.loc
            self.commits += other.commits
            self.files += other.files
        except (TypeError, AttributeError) as e:
            get_logger(__name__).error(f"Error adding AuthorStats: {e}")
            raise

    def to_dict(self) -> dict[str, int]:
        """Convert to dictionary."""
        try:
            return {"loc": self.loc, "commits": self.commits, "files": self.files}
        except (TypeError, AttributeError) as e:
            get_logger(__name__).error(f"Error converting AuthorStats to dict: {e}")
            raise


@dataclass
class RepositoryStats:
    """Represents statistics for a single repository."""

    display_name: str
    guillermo_stats: AuthorStats
    repo_totals: AuthorStats
    language_stats: dict[str, dict[str, int]] | None = None

    def __post_init__(self) -> None:
        if self.language_stats is None:
            self.language_stats = {}

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        try:
            return {
                "display_name": self.display_name,
                "guillermo_stats": self.guillermo_stats.to_dict(),
                "repo_totals": self.repo_totals.to_dict(),
                "language_stats": self.language_stats,
            }
        except (TypeError, AttributeError) as e:
            get_logger(__name__).error(f"Error converting RepositoryStats to dict: {e}")
            raise


@dataclass
class UnifiedStats:
    """Represents unified statistics across all repositories."""

    total_commits: int = 0
    total_files: int = 0
    total_loc: int = 0
    repos_processed: int = 0
    guillermo_unified: AuthorStats | None = None
    repo_breakdown: dict[str, RepositoryStats] | None = None
    unified_language_stats: dict[str, dict[str, int]] | None = None
    other_unknown_breakdown: dict[str, int] | None = (
        None  # New: breakdown of other/unknown
    )
    validation_results: dict[str, Any] | None = None  # New: validation results

    def __post_init__(self) -> None:
        if self.guillermo_unified is None:
            self.guillermo_unified = AuthorStats()
        if self.repo_breakdown is None:
            self.repo_breakdown = {}
        if self.unified_language_stats is None:
            self.unified_language_stats = {}
        if self.other_unknown_breakdown is None:
            self.other_unknown_breakdown = {}
        if self.validation_results is None:
            self.validation_results = {}


class AuthorMatcher:
    """Handles author pattern matching and classification."""

    def __init__(self, guillermo_patterns: list[str], bot_patterns: list[str]) -> None:
        """
        Initialize the author matcher.

        Args:
            guillermo_patterns: Regex patterns to match Guillermo's authorship
            bot_patterns: Regex patterns to match bot authors
        """
        self.logger = get_logger(__name__)

        try:
            self.guillermo_patterns = guillermo_patterns
            self.bot_patterns = bot_patterns

            # Validate patterns
            for pattern in guillermo_patterns + bot_patterns:
                re.compile(pattern, re.IGNORECASE)

            self.logger.info(
                f"AuthorMatcher initialized with {len(guillermo_patterns)} Guillermo patterns and {len(bot_patterns)} bot patterns"
            )

        except re.error as e:
            log_and_raise(
                StatsProcessingError,
                f"Invalid regex pattern in AuthorMatcher: {e}",
                error_code="INVALID_REGEX_PATTERN",
            )
        except Exception as e:
            log_and_raise(
                StatsProcessingError,
                f"Error initializing AuthorMatcher: {e}",
                error_code="INITIALIZATION_ERROR",
            )

    def is_guillermo(self, author_name: str) -> bool:
        """
        Check if an author name matches Guillermo patterns.

        Args:
            author_name: Author name to check

        Returns:
            True if matches Guillermo patterns
        """
        try:
            if not author_name:
                return False

            return any(
                re.search(pattern, str(author_name), re.IGNORECASE)
                for pattern in self.guillermo_patterns
            )

        except (TypeError, AttributeError, re.error) as e:
            self.logger.error(f"Error checking if '{author_name}' is Guillermo: {e}")
            return False

    def is_bot(self, author_name: str) -> bool:
        """
        Check if an author name matches bot patterns.

        Args:
            author_name: Author name to check

        Returns:
            True if matches bot patterns
        """
        try:
            if not author_name:
                return False

            return any(
                re.search(pattern, str(author_name), re.IGNORECASE)
                for pattern in self.bot_patterns
            )

        except (TypeError, AttributeError, re.error) as e:
            self.logger.error(f"Error checking if '{author_name}' is bot: {e}")
            return False

    def classify_author(self, author_name: str) -> str:
        """
        Classify an author as 'guillermo', 'bot', or 'other'.

        Args:
            author_name: Author name to classify

        Returns:
            Classification string
        """
        try:
            if not author_name:
                self.logger.warning(
                    "Empty author name provided, classifying as 'other'"
                )
                return "other"

            if self.is_bot(author_name):
                return "bot"
            elif self.is_guillermo(author_name):
                return "guillermo"
            else:
                return "other"

        except (TypeError, AttributeError) as e:
            self.logger.error(f"Error classifying author '{author_name}': {e}")
            return "other"


class StatsProcessor:
    """Main statistics processing class."""

    def __init__(self, author_matcher: AuthorMatcher) -> None:
        """
        Initialize the stats processor.

        Args:
            author_matcher: AuthorMatcher instance for classifying authors
        """
        self.logger = get_logger(__name__)
        self.author_matcher = author_matcher

        if not author_matcher:
            log_and_raise(
                StatsProcessingError,
                "AuthorMatcher is required for StatsProcessor",
                error_code="MISSING_AUTHOR_MATCHER",
            )

    def process_repository_data(
        self, authors: list[tuple[str, int, int, int]], display_name: str
    ) -> RepositoryStats:
        """
        Process author data for a single repository.

        Args:
            authors: List of (author_name, loc, commits, files) tuples
            display_name: Display name for the repository

        Returns:
            RepositoryStats object with processed data
        """
        try:
            guillermo_stats = AuthorStats()
            repo_totals = AuthorStats()
            language_stats: dict[str, dict[str, int]] = {}

            for author_name, loc, commits, files in authors:
                try:
                    # Add to repo totals
                    repo_totals.loc += loc
                    repo_totals.commits += commits
                    repo_totals.files += files

                    # Classify author and add to appropriate stats
                    author_type = self.author_matcher.classify_author(author_name)

                    if author_type == "guillermo":
                        guillermo_stats.loc += loc
                        guillermo_stats.commits += commits
                        guillermo_stats.files += files

                except (TypeError, ValueError, AttributeError) as e:
                    self.logger.warning(
                        f"Error processing author data for '{author_name}': {e}"
                    )
                    continue

            return RepositoryStats(
                display_name=display_name,
                guillermo_stats=guillermo_stats,
                repo_totals=repo_totals,
                language_stats=language_stats,
            )

        except (TypeError, AttributeError, ValueError) as e:
            log_and_raise(
                StatsProcessingError,
                f"Error processing repository data for '{display_name}': {e}",
                error_code="REPO_DATA_PROCESSING_ERROR",
            )
            return RepositoryStats(
                display_name=display_name,
                guillermo_stats=AuthorStats(),
                repo_totals=AuthorStats(),
                language_stats={},
            )

    def aggregate_repository_stats(
        self, repository_stats_list: list[RepositoryStats]
    ) -> UnifiedStats:
        """
        Aggregate statistics from multiple repositories.

        Args:
            repository_stats_list: List of RepositoryStats objects

        Returns:
            UnifiedStats object with aggregated data
        """
        try:
            unified_stats = UnifiedStats()
            self.logger.info(f"Aggregating stats from {len(repository_stats_list)} repositories")

            for repo_stats in repository_stats_list:
                self.logger.info(f"Processing repository: {repo_stats.display_name}")
                try:
                    # Add to unified totals
                    unified_stats.total_loc += repo_stats.repo_totals.loc
                    unified_stats.total_commits += repo_stats.repo_totals.commits
                    unified_stats.total_files += repo_stats.repo_totals.files

                    # Add to Guillermo's unified stats
                    unified_stats.guillermo_unified.add(repo_stats.guillermo_stats)

                    # Add to repo breakdown
                    unified_stats.repo_breakdown[repo_stats.display_name] = repo_stats

                    # Aggregate language stats
                    if repo_stats.language_stats:
                        for lang, stats in repo_stats.language_stats.items():
                            if lang not in unified_stats.unified_language_stats:
                                unified_stats.unified_language_stats[lang] = {
                                    "loc": 0,
                                    "commits": 0,
                                    "files": 0,
                                }
                            unified_stats.unified_language_stats[lang][
                                "loc"
                            ] += stats.get("loc", 0)
                            unified_stats.unified_language_stats[lang][
                                "commits"
                            ] += stats.get("commits", 0)
                            unified_stats.unified_language_stats[lang][
                                "files"
                            ] += stats.get("files", 0)

                    unified_stats.repos_processed += 1
                    self.logger.info(f"Successfully processed {repo_stats.display_name}")

                except (TypeError, AttributeError, KeyError) as e:
                    self.logger.warning(
                        f"Error aggregating stats for '{repo_stats.display_name}': {e}"
                    )
                    continue

            self.logger.info(f"Aggregation complete. Processed {unified_stats.repos_processed} repositories")
            self.logger.info(f"Total LOC: {unified_stats.total_loc}, Total commits: {unified_stats.total_commits}")
            self.logger.info(f"Repo breakdown contains {len(unified_stats.repo_breakdown)} repositories")

            return unified_stats

        except (TypeError, AttributeError, ValueError) as e:
            log_and_raise(
                StatsProcessingError,
                f"Error aggregating repository stats: {e}",
                error_code="AGGREGATION_ERROR",
            )
            return UnifiedStats()

    def calculate_distribution_percentages(
        self, stats: AuthorStats, totals: AuthorStats
    ) -> tuple[float, float, float]:
        """
        Calculate distribution percentages for an author's contributions.

        Args:
            stats: Author's statistics
            totals: Total repository statistics

        Returns:
            Tuple of (loc_percentage, commits_percentage, files_percentage)
        """
        try:
            loc_pct = (stats.loc / totals.loc * 100) if totals.loc > 0 else 0
            commits_pct = (
                (stats.commits / totals.commits * 100) if totals.commits > 0 else 0
            )
            files_pct = (stats.files / totals.files * 100) if totals.files > 0 else 0

            return (loc_pct, commits_pct, files_pct)

        except Exception as e:
            self.logger.error(f"Error calculating distribution percentages: {e}")
            return (0.0, 0.0, 0.0)

    def validate_unified_stats(self, stats: UnifiedStats) -> list[str]:
        """
        Validate unified statistics and return any validation errors.

        Args:
            stats: UnifiedStats object to validate

        Returns:
            List of validation error messages
        """
        try:
            errors = []

            if stats.guillermo_unified and stats.guillermo_unified.loc == 0:
                errors.append("No Guillermo contributions found")

            if stats.repos_processed == 0:
                errors.append("No repositories processed")

            if stats.total_loc == 0:
                errors.append("No lines of code found")

            if not stats.repo_breakdown:
                errors.append("No repository breakdown data")

            if errors:
                self.logger.warning(f"Validation found {len(errors)} issues: {errors}")
            else:
                self.logger.info("Unified stats validation passed")

            return errors

        except Exception as e:
            self.logger.error(f"Error validating unified stats: {e}")
            return ["Validation error occurred"]

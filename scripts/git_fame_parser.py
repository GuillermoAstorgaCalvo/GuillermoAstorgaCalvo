"""
Git Fame Parser Module
Handles parsing and processing of git fame output data.
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Any

from error_handling import (
    get_logger,
)

# Set up logging for this module
logger = get_logger(__name__)


class GitFameParser:
    """Handles git fame execution and data parsing."""

    def __init__(self, timeout_seconds: int = 120):
        """
        Initialize the git fame parser.
        Args:
            timeout_seconds: Timeout for git fame execution
        """
        self.timeout_seconds = timeout_seconds
        self._check_git_fame_version()

    def _check_git_fame_version(self) -> bool:
        """Check if git fame is available and get its version."""
        try:
            # nosec B603: git-fame is a trusted tool, args are hardcoded
            # nosec B607: git-fame is a standard tool installed via package manager
            result = subprocess.run(  # nosec B603 B607
                ["git-fame", "--version"], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                logger.info(f"Git fame version: {version}")
                logger.debug("Git fame version check completed")
                return True
            else:
                logger.error(f"Git fame version check failed: {result.stderr}")
                return False
        except (
            subprocess.TimeoutExpired,
            subprocess.CalledProcessError,
            FileNotFoundError,
        ) as e:
            logger.error(f"Git fame not found or not accessible: {e}")
            return False
        except (TypeError, ValueError) as e:
            logger.error(f"Error checking git fame version: {e}")
            return False

    def execute_git_fame(
        self, repo_path: str, output_format: str = "json", by_type: bool = False
    ) -> dict[str, Any] | None:
        """
        Execute git fame on a repository and return parsed data.
        Args:
            repo_path: Path to the git repository
            output_format: Output format for git fame (default: json)
            by_type: Whether to include --bytype flag for per-extension stats
        Returns:
            Parsed git fame data or None if execution failed
        """
        # Input validation
        if not isinstance(repo_path, str) or not repo_path.strip():
            logger.error("Invalid repository path: must be a non-empty string")
            return None

        if not isinstance(output_format, str) or output_format not in [
            "json",
            "csv",
            "tsv",
        ]:
            logger.error(
                f"Invalid output format: {output_format}. Must be one of: json, csv, tsv"
            )
            return None

        if not isinstance(by_type, bool):
            logger.error(f"Invalid by_type parameter: {by_type}. Must be a boolean")
            return None

        # Sanitize repo_path to prevent path traversal
        repo_path = os.path.abspath(repo_path.strip())

        original_cwd = os.getcwd()

        try:
            if not Path(repo_path).exists():
                logger.error(f"Repository path does not exist: {repo_path}")
                return None

            # Verify it's actually a git repository
            if not Path(repo_path, ".git").exists():
                logger.error(f"Path is not a git repository: {repo_path}")
                return None

            os.chdir(repo_path)

            # Build git fame command with optimizations for speed
            cmd = ["git", "fame", "--format", output_format]
            if by_type:
                cmd.append("--bytype")

            # Execute git fame command
            try:
                # nosec B603: cmd contains trusted git commands with validated args
                result = subprocess.run(  # nosec B603
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout_seconds,
                    cwd=repo_path,
                )

                logger.debug(f"Executing git fame command: {' '.join(cmd)}")

                if result.returncode != 0:
                    logger.error(
                        f"Git fame execution failed with return code {result.returncode}"
                    )
                    logger.error(f"Error output: {result.stderr}")
                    return None

                if not result.stdout.strip():
                    logger.warning("Git fame produced no output")
                    return None

                # Parse JSON output
                try:
                    data = json.loads(result.stdout)
                    if isinstance(data, dict):
                        return data
                    else:
                        logger.error("Git fame output is not a dictionary")
                        return None
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse git fame JSON output: {e}")
                    logger.debug(f"Raw output: {result.stdout[:500]}...")
                    return None

            except subprocess.TimeoutExpired as e:
                logger.error(
                    f"Git fame execution timed out after {self.timeout_seconds} seconds: {e}"
                )
                return None
            except subprocess.CalledProcessError as e:
                logger.error(f"Git fame process error: {e}")
                return None
            except (TypeError, ValueError, OSError) as e:
                logger.error(f"Error executing git fame: {e}")
                return None

        except Exception as e:
            logger.error(
                f"Unexpected error during git fame execution: {e}",
                extra={"repo_path": repo_path},
            )
            return None
        finally:
            os.chdir(original_cwd)

    def parse_author_data(self, author_data: Any) -> tuple[str, int, int, int] | None:
        """
        Parse individual author data from git fame output.
        Args:
            author_data: Raw author data from git fame (dict or list)
        Returns:
            Tuple of (author_name, loc, commits, files) or None if parsing failed
        """
        try:
            if isinstance(author_data, dict):
                author_name = author_data.get("author", "")
                loc = max(0, author_data.get("loc", 0))
                commits = max(0, author_data.get("commits", 0))
                files = max(0, author_data.get("files", 0))
            elif isinstance(author_data, list) and len(author_data) >= 4:
                author_name = author_data[0] if len(author_data) > 0 else ""
                loc = max(
                    0, int(author_data[1]) if str(author_data[1]).isdigit() else 0
                )
                commits = max(
                    0, int(author_data[2]) if str(author_data[2]).isdigit() else 0
                )
                files = max(
                    0, int(author_data[3]) if str(author_data[3]).isdigit() else 0
                )
            else:
                logger.warning(f"Invalid author data format: {type(author_data)}")
                return None

            return (author_name, loc, commits, files)

        except (ValueError, IndexError, TypeError) as e:
            logger.warning(
                f"Failed to parse author data: {e}",
                extra={"author_data": str(author_data)},
            )
            return None

    def get_repository_summary(self, data: dict[str, Any]) -> dict[str, int]:
        """
        Extract repository summary statistics from git fame data.
        Args:
            data: Parsed git fame data
        Returns:
            Dictionary with total_loc, total_commits, total_files
        """
        try:
            summary = {
                "total_loc": data.get("total_loc", 0),
                "total_commits": data.get("total_commits", 0),
                "total_files": data.get("total_files", 0),
            }
            logger.debug(f"Repository summary extracted: {summary}")
            return summary
        except (TypeError, AttributeError, KeyError) as e:
            logger.error(f"Failed to extract repository summary: {e}")
            return {"total_loc": 0, "total_commits": 0, "total_files": 0}

    def validate_git_fame_data(self, data: dict[str, Any]) -> bool:
        """
        Validate that git fame data contains expected fields.
        Args:
            data: Parsed git fame data
        Returns:
            True if data is valid, False otherwise
        """
        try:
            if not isinstance(data, dict):
                logger.warning("Git fame data is not a dictionary")
                return False

            # Check for required fields
            required_fields = ["data"]
            for field in required_fields:
                if field not in data:
                    logger.warning(f"Missing required field in git fame data: {field}")
                    return False

            # Check that data is a list
            if not isinstance(data.get("data"), list):
                logger.warning("Git fame data 'data' field is not a list")
                return False

            logger.debug("Git fame data validation passed")
            return True

        except (TypeError, AttributeError, KeyError) as e:
            logger.error(f"Error during git fame data validation: {e}")
            return False

    def extract_authors(self, data: dict[str, Any]) -> list[tuple[str, int, int, int]]:
        """
        Extract all author data from git fame output.
        Args:
            data: Parsed git fame data
        Returns:
            List of tuples (author_name, loc, commits, files)
        """
        authors = []

        try:
            for author_data in data.get("data", []):
                parsed_author = self.parse_author_data(author_data)
                if parsed_author:
                    authors.append(parsed_author)

            logger.info(f"Extracted {len(authors)} authors from git fame data")
            return authors

        except (TypeError, AttributeError, KeyError) as e:
            logger.error(f"Failed to extract authors from git fame data: {e}")
            return []

    def extract_extension_stats(
        self, data: dict[str, Any]
    ) -> dict[str, dict[str, int | float]]:
        """
        Extract per-extension statistics from git fame --bytype output.
        Args:
            data: Parsed git fame data with --bytype flag
        Returns:
            Dictionary with extension as key and stats as value
        """
        extension_stats = {}

        try:
            # Git fame --bytype puts extension stats in the 'total' section
            total_data = data.get("total", {})

            # Extract file extensions and their stats
            for key, value in total_data.items():
                if key.startswith(".") or key in [
                    "Makefile",
                    "Dockerfile",
                    "CMakeLists.txt",
                    "package.json",
                    "requirements.txt",
                    "go.mod",
                    "Cargo.toml",
                    "composer.json",
                    "Gemfile",
                ]:
                    # This is a file extension or special filename
                    extension = key
                    loc = value if isinstance(value, int | float) else 0

                    # For --bytype, we get LOC per extension
                    # Estimate file count based on LOC (roughly 1 file per 500 LOC)
                    # This is a reasonable estimate since we can't get exact file counts from --bytype
                    estimated_files = max(1, int(loc / 500))

                    extension_stats[extension] = {
                        "loc": loc,
                        "files": estimated_files,
                        "commits": 0,  # Not available in --bytype mode
                    }

            logger.info(f"Extracted stats for {len(extension_stats)} file extensions")
            return extension_stats

        except (TypeError, AttributeError, KeyError, ValueError) as e:
            logger.error(f"Failed to extract extension stats: {e}")
            return {}

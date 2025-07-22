#!/usr/bin/env python3
"""
Dynamic Tech Stack Analyzer
Analyzes dependencies across all repositories to generate a fully dynamic tech stack.
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import yaml
from dependency_analyzer import DependencyAnalyzer
from error_handling import get_logger, with_error_context
from skillicon_mapper import SkilliconMapper

logger = get_logger(__name__)


class DynamicTechStackAnalyzer:
    """Analyzes dependencies across all repositories to generate dynamic tech stack."""

    def __init__(self) -> None:
        """Initialize the dynamic tech stack analyzer."""
        self.dependency_analyzer = DependencyAnalyzer()
        self.skillicon_mapper = SkilliconMapper()
        self.config = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        """Load configuration from config.yml."""
        try:
            config_path = Path(__file__).parent.parent / "config.yml"
            with open(config_path, encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {"repositories": []}

    @with_error_context({"component": "dynamic_tech_stack_analyzer"})
    def clone_repository(
        self, repo_name: str, organization: str, token: str | None = None
    ) -> Path | None:
        """Clone a repository to a temporary directory."""
        try:
            # Create temporary directory
            temp_dir = Path(tempfile.mkdtemp(prefix=f"repo_{repo_name}_"))

            # Build clone URL
            if token:
                clone_url = f"https://{token}@github.com/{organization}/{repo_name}.git"
            else:
                clone_url = f"https://github.com/{organization}/{repo_name}.git"

            # Clone repository
            logger.info(f"Cloning {organization}/{repo_name} to {temp_dir}")
            result = subprocess.run(
                ["git", "clone", "--depth", "1", clone_url, str(temp_dir)],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes timeout
            )

            if result.returncode != 0:
                logger.error(f"Failed to clone {repo_name}: {result.stderr}")
                return None

            return temp_dir

        except Exception as e:
            logger.error(f"Error cloning {repo_name}: {e}")
            return None

    @with_error_context({"component": "dynamic_tech_stack_analyzer"})
    def analyze_repository_dependencies(self, repo_path: Path) -> dict[str, set[str]]:
        """Analyze dependencies in a single repository."""
        if not repo_path or not repo_path.exists():
            return {
                "frontend": set(),
                "backend": set(),
                "database": set(),
                "devops": set(),
                "ai_ml": set(),
            }

        try:
            return self.dependency_analyzer.analyze_repository_dependencies(repo_path)
        except Exception as e:
            logger.error(f"Error analyzing dependencies in {repo_path}: {e}")
            return {
                "frontend": set(),
                "backend": set(),
                "database": set(),
                "devops": set(),
                "ai_ml": set(),
            }

    @with_error_context({"component": "dynamic_tech_stack_analyzer"})
    def analyze_all_repositories(self) -> dict[str, Any]:
        """Analyze dependencies across all configured repositories."""
        all_technologies: dict[str, set[str]] = {
            "frontend": set(),
            "backend": set(),
            "database": set(),
            "devops": set(),
            "ai_ml": set(),
        }

        repositories = self.config.get("repositories", [])
        logger.info(f"Analyzing {len(repositories)} repositories")

        for repo_config in repositories:
            repo_name = repo_config.get("name")
            organization = repo_config.get("organization")
            token_type = repo_config.get("token_type", "public")

            if not repo_name or not organization:
                logger.warning(
                    f"Skipping repository with missing name or organization: {repo_config}"
                )
                continue

            logger.info(f"Processing repository: {organization}/{repo_name}")

            # Get token if needed
            token = None
            if token_type == "private":
                token = os.environ.get("GITHUB_TOKEN")
                if not token:
                    logger.warning(
                        f"No GitHub token found for private repository {repo_name}"
                    )
                    continue
            elif token_type == "personal":
                token = os.environ.get("PERSONAL_GITHUB_TOKEN")
                if not token:
                    logger.warning(
                        f"No personal GitHub token found for repository {repo_name}"
                    )
                    continue

            # Clone repository
            repo_path = self.clone_repository(repo_name, organization, token)
            if not repo_path:
                logger.warning(f"Failed to clone {repo_name}, skipping")
                continue

            try:
                # Analyze dependencies
                repo_tech = self.analyze_repository_dependencies(repo_path)

                # Merge technologies
                for category, techs in repo_tech.items():
                    all_technologies[category].update(techs)

                logger.info(
                    f"Found {sum(len(techs) for techs in repo_tech.values())} technologies in {repo_name}"
                )

            finally:
                # Clean up temporary directory
                try:
                    import shutil

                    shutil.rmtree(repo_path)
                except Exception as e:
                    logger.warning(f"Failed to clean up {repo_path}: {e}")

        # Convert sets to sorted lists and map to skillicons
        basic_tech_stack = {
            cat: {"technologies": sorted(techs), "count": len(techs)}
            for cat, techs in all_technologies.items()
        }

        # Map to valid skillicon IDs
        mapped_tech_stack = self.skillicon_mapper.map_technologies(basic_tech_stack)

        logger.info(
            f"Total technologies found: {sum(len(data.get('technologies', [])) for data in mapped_tech_stack.values())}"
        )

        return mapped_tech_stack

    @with_error_context({"component": "dynamic_tech_stack_analyzer"})
    def generate_dynamic_tech_stack(self) -> dict[str, Any]:
        """Generate dynamic tech stack and save to file."""
        try:
            # Analyze all repositories
            tech_stack = self.analyze_all_repositories()

            # Add metadata
            result = {
                "timestamp": self._get_timestamp(),
                "metadata": {
                    "version": "3.0",
                    "generated_by": "Dynamic Tech Stack Analyzer",
                    "data_source": "Multi-Repository Dependency Analysis",
                },
                "tech_stack_analysis": tech_stack,
                "repository_count": len(self.config.get("repositories", [])),
                "total_technologies": sum(
                    len(data.get("technologies", [])) for data in tech_stack.values()
                ),
            }

            # Save to file
            output_file = Path(__file__).parent.parent / "dynamic_tech_stack.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            logger.info(f"Dynamic tech stack saved to {output_file}")
            return result

        except Exception as e:
            logger.error(f"Failed to generate dynamic tech stack: {e}")
            return {}

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime

        return datetime.utcnow().isoformat() + "Z"


def main() -> None:
    """Main function to generate dynamic tech stack."""
    analyzer = DynamicTechStackAnalyzer()
    result = analyzer.generate_dynamic_tech_stack()

    if result:
        print("✅ Dynamic tech stack generated successfully!")
        print(
            f"📊 Found {result.get('total_technologies', 0)} technologies across {result.get('repository_count', 0)} repositories"
        )

        tech_stack = result.get("tech_stack_analysis", {})
        for category, data in tech_stack.items():
            techs = data.get("technologies", [])
            if techs:
                print(
                    f"🔧 {category.title()}: {', '.join(techs[:5])}{'...' if len(techs) > 5 else ''}"
                )
    else:
        print("❌ Failed to generate dynamic tech stack")


if __name__ == "__main__":
    main()

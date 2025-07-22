#!/usr/bin/env python3
"""
API-Based Repository Analyzer
Analyzes repositories using GitHub API instead of cloning them.
"""

import base64
import json
from pathlib import Path
from typing import Any

import requests
import yaml
from dependency_analyzer import DependencyAnalyzer
from env_manager import env_manager
from error_handling import get_logger, with_error_context
from skillicon_mapper import SkilliconMapper

logger = get_logger(__name__)


class APIBasedRepositoryAnalyzer:
    """Analyzes repositories using GitHub API for dependency analysis."""

    def __init__(self) -> None:
        """Initialize the API-based repository analyzer."""
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

    def _get_github_token(self, token_type: str) -> str | None:
        """Get appropriate GitHub token based on token type."""
        return env_manager.get_token_by_type(token_type)

    def _make_github_request(self, url: str, token: str | None = None) -> dict | None:
        """Make a GitHub API request with proper headers."""
        try:
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "GuillermoAstorgaCalvo-TechStackAnalyzer",
            }

            if token:
                headers["Authorization"] = f"token {token}"

            response = requests.get(url, headers=headers, timeout=30)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                logger.warning(f"Repository not found: {url}")
                return None
            elif response.status_code == 403:
                logger.warning(f"Access denied: {url} - Check token permissions")
                return None
            else:
                logger.warning(f"GitHub API error {response.status_code}: {url}")
                return None

        except Exception as e:
            logger.error(f"Error making GitHub request to {url}: {e}")
            return None

    def _get_repository_content(
        self, org: str, repo: str, path: str, token: str | None = None
    ) -> str | None:
        """Get file content from GitHub repository."""
        try:
            url = f"https://api.github.com/repos/{org}/{repo}/contents/{path}"
            content_data = self._make_github_request(url, token)

            if content_data and "content" in content_data:
                # Decode base64 content
                content = base64.b64decode(content_data["content"]).decode("utf-8")
                return content

            return None

        except Exception as e:
            logger.error(f"Error getting content for {org}/{repo}/{path}: {e}")
            return None

    def _analyze_dependency_file_content(
        self, content: str, file_type: str
    ) -> dict[str, set[str]]:
        """Analyze dependency file content and extract technologies."""
        categories = {
            "frontend": set(),
            "backend": set(),
            "database": set(),
            "devops": set(),
            "ai_ml": set(),
        }

        try:
            if file_type == "package.json":
                data = json.loads(content)
                deps = data.get("dependencies", {})
                dev_deps = data.get("devDependencies", {})
                all_deps = {**deps, **dev_deps}

                for dep_name in all_deps.keys():
                    dep_lower = dep_name.lower()
                    # Use the existing technology mappings from DependencyAnalyzer
                    if dep_lower in self.dependency_analyzer.frontend_tech:
                        categories["frontend"].add(
                            self.dependency_analyzer.frontend_tech[dep_lower]
                        )
                    elif dep_lower in self.dependency_analyzer.backend_tech:
                        categories["backend"].add(
                            self.dependency_analyzer.backend_tech[dep_lower]
                        )
                    elif dep_lower in self.dependency_analyzer.database_tech:
                        categories["database"].add(
                            self.dependency_analyzer.database_tech[dep_lower]
                        )
                    elif dep_lower in self.dependency_analyzer.devops_tech:
                        categories["devops"].add(
                            self.dependency_analyzer.devops_tech[dep_lower]
                        )
                    elif dep_lower in self.dependency_analyzer.ai_ml_tech:
                        categories["ai_ml"].add(
                            self.dependency_analyzer.ai_ml_tech[dep_lower]
                        )

            elif file_type == "requirements.txt":
                for line in content.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        package_name = (
                            line.split("==")[0]
                            .split(">=")[0]
                            .split("<=")[0]
                            .split("~=")[0]
                            .split("!=")[0]
                            .strip()
                        )
                        package_lower = package_name.lower()

                        if package_lower in self.dependency_analyzer.backend_tech:
                            categories["backend"].add(
                                self.dependency_analyzer.backend_tech[package_lower]
                            )
                        elif package_lower in self.dependency_analyzer.database_tech:
                            categories["database"].add(
                                self.dependency_analyzer.database_tech[package_lower]
                            )
                        elif package_lower in self.dependency_analyzer.devops_tech:
                            categories["devops"].add(
                                self.dependency_analyzer.devops_tech[package_lower]
                            )
                        elif package_lower in self.dependency_analyzer.ai_ml_tech:
                            categories["ai_ml"].add(
                                self.dependency_analyzer.ai_ml_tech[package_lower]
                            )

            elif file_type == "pyproject.toml":
                # Simple pattern matching for pyproject.toml
                import re

                deps_pattern = r"\[tool\.poetry\.dependencies\]\s*\n(.*?)(?=\n\[|\Z)"
                matches = re.findall(deps_pattern, content, re.DOTALL)
                for match in matches:
                    lines = match.strip().split("\n")
                    for line in lines:
                        line = line.strip()
                        if "=" in line and not line.startswith("#"):
                            package_name = (
                                line.split("=")[0].strip().strip('"').strip("'")
                            )
                            package_lower = package_name.lower()

                            if package_lower in self.dependency_analyzer.backend_tech:
                                categories["backend"].add(
                                    self.dependency_analyzer.backend_tech[package_lower]
                                )
                            elif (
                                package_lower in self.dependency_analyzer.database_tech
                            ):
                                categories["database"].add(
                                    self.dependency_analyzer.database_tech[
                                        package_lower
                                    ]
                                )
                            elif package_lower in self.dependency_analyzer.devops_tech:
                                categories["devops"].add(
                                    self.dependency_analyzer.devops_tech[package_lower]
                                )
                            elif package_lower in self.dependency_analyzer.ai_ml_tech:
                                categories["ai_ml"].add(
                                    self.dependency_analyzer.ai_ml_tech[package_lower]
                                )

        except Exception as e:
            logger.error(f"Error analyzing {file_type} content: {e}")

        return categories

    def _detect_technologies_from_repository_structure(
        self, org: str, repo: str, token: str | None = None
    ) -> dict[str, set[str]]:
        """Detect technologies from repository structure using GitHub API."""
        categories = {
            "frontend": set(),
            "backend": set(),
            "database": set(),
            "devops": set(),
            "ai_ml": set(),
        }

        try:
            # Get repository contents
            url = f"https://api.github.com/repos/{org}/{repo}/contents"
            contents = self._make_github_request(url, token)

            if not contents:
                return categories

            # Check for common files and directories
            for item in contents:
                name = item.get("name", "").lower()
                item_type = item.get("type", "file")

                # Frontend technologies
                if name.endswith((".jsx", ".tsx")):
                    categories["frontend"].add("react")
                elif name.endswith(".vue"):
                    categories["frontend"].add("vue")
                elif name == "angular.json":
                    categories["frontend"].add("angular")
                elif name in ["tailwind.config.js", "tailwind.config.ts"]:
                    categories["frontend"].add("tailwind")
                elif name in ["next.config.js", "next.config.ts"]:
                    categories["frontend"].add("nextjs")
                elif name in ["nuxt.config.js", "nuxt.config.ts"]:
                    categories["frontend"].add("nuxt")

                # Backend technologies
                elif name.endswith(".py"):
                    categories["backend"].add("python")
                elif name.endswith((".js", ".ts")) and item_type == "file":
                    categories["backend"].add("nodejs")
                elif name.endswith(".java"):
                    categories["backend"].add("java")
                elif name.endswith(".go"):
                    categories["backend"].add("go")
                elif name.endswith(".rs"):
                    categories["backend"].add("rust")

                # DevOps technologies
                elif name == "dockerfile":
                    categories["devops"].add("docker")
                elif name in ["docker-compose.yml", "docker-compose.yaml"]:
                    categories["devops"].add("docker")
                elif name.endswith(".tf"):
                    categories["devops"].add("terraform")
                elif name == ".github" and item_type == "dir":
                    categories["devops"].add("github")
                    categories["devops"].add("githubactions")

                # AI/ML technologies
                elif name.endswith(".ipynb"):
                    categories["ai_ml"].add("jupyter")
                    categories["ai_ml"].add("pandas")
                    categories["ai_ml"].add("numpy")

                # Database technologies
                elif name.endswith((".sql", ".db")):
                    categories["database"].add("sqlite")

        except Exception as e:
            logger.error(f"Error detecting technologies from repository structure: {e}")

        return categories

    @with_error_context({"component": "api_based_repository_analyzer"})
    def analyze_repository_via_api(
        self, org: str, repo: str, token_type: str = "public"
    ) -> dict[str, set[str]]:
        """Analyze a single repository using GitHub API."""
        all_technologies = {
            "frontend": set(),
            "backend": set(),
            "database": set(),
            "devops": set(),
            "ai_ml": set(),
        }

        try:
            token = self._get_github_token(token_type)
            logger.info(f"Analyzing repository: {org}/{repo}")

            # 1. Analyze dependency files
            dependency_files = [
                ("package.json", "package.json"),
                ("requirements.txt", "requirements.txt"),
                ("pyproject.toml", "pyproject.toml"),
                ("Cargo.toml", "Cargo.toml"),
                ("pom.xml", "pom.xml"),
                ("go.mod", "go.mod"),
            ]

            for file_type, file_path in dependency_files:
                content = self._get_repository_content(org, repo, file_path, token)
                if content:
                    logger.info(f"Found {file_type} in {org}/{repo}")
                    file_techs = self._analyze_dependency_file_content(
                        content, file_type
                    )
                    for category, techs in file_techs.items():
                        all_technologies[category].update(techs)

            # 2. Detect technologies from repository structure
            structure_techs = self._detect_technologies_from_repository_structure(
                org, repo, token
            )
            for category, techs in structure_techs.items():
                all_technologies[category].update(techs)

            # 3. Get repository description and topics for additional hints
            repo_info = self._make_github_request(
                f"https://api.github.com/repos/{org}/{repo}", token
            )
            if repo_info:
                description = repo_info.get("description", "")
                topics = repo_info.get("topics", [])

                if description or topics:
                    full_description = f"{description} {' '.join(topics)}"
                    # Use pattern matching to extract technologies from description
                    from enhanced_dependency_analyzer import EnhancedDependencyAnalyzer

                    enhanced_analyzer = EnhancedDependencyAnalyzer()
                    desc_techs = (
                        enhanced_analyzer._detect_technologies_from_description(
                            full_description
                        )
                    )

                    for category, techs in desc_techs.items():
                        all_technologies[category].update(techs)

            logger.info(
                f"Found {sum(len(techs) for techs in all_technologies.values())} technologies in {org}/{repo}"
            )

        except Exception as e:
            logger.error(f"Error analyzing repository {org}/{repo}: {e}")

        return all_technologies

    @with_error_context({"component": "api_based_repository_analyzer"})
    def analyze_all_repositories(self) -> dict[str, Any]:
        """Analyze all configured repositories using GitHub API."""
        all_technologies = {
            "frontend": set(),
            "backend": set(),
            "database": set(),
            "devops": set(),
            "ai_ml": set(),
        }

        repositories = self.config.get("repositories", [])
        logger.info(f"Analyzing {len(repositories)} repositories via API")

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

            # Analyze repository via API
            repo_tech = self.analyze_repository_via_api(
                organization, repo_name, token_type
            )

            # Merge technologies
            for category, techs in repo_tech.items():
                all_technologies[category].update(techs)

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

    @with_error_context({"component": "api_based_repository_analyzer"})
    def generate_api_based_tech_stack(self) -> dict[str, Any]:
        """Generate API-based tech stack and save to file."""
        try:
            # Analyze all repositories
            tech_stack = self.analyze_all_repositories()

            # Add metadata
            result = {
                "timestamp": self._get_timestamp(),
                "metadata": {
                    "version": "4.0",
                    "generated_by": "API-Based Repository Analyzer",
                    "data_source": "GitHub API Analysis",
                },
                "tech_stack_analysis": tech_stack,
                "repository_count": len(self.config.get("repositories", [])),
                "total_technologies": sum(
                    len(data.get("technologies", [])) for data in tech_stack.values()
                ),
            }

            # Save to file
            output_file = Path(__file__).parent.parent / "api_based_tech_stack.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            logger.info(f"API-based tech stack saved to {output_file}")
            return result

        except Exception as e:
            logger.error(f"Failed to generate API-based tech stack: {e}")
            return {}

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime

        return datetime.utcnow().isoformat() + "Z"


def main() -> None:
    """Main function to generate API-based tech stack."""
    analyzer = APIBasedRepositoryAnalyzer()
    result = analyzer.generate_api_based_tech_stack()

    if result:
        print("✅ API-based tech stack generated successfully!")
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
        print("❌ Failed to generate API-based tech stack")


if __name__ == "__main__":
    main()

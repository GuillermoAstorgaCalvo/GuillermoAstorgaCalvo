#!/usr/bin/env python3
"""
Enhanced Dependency Analyzer
Provides comprehensive tech stack analysis based on project descriptions and existing data.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
import yaml
from dependency_analyzer import DependencyAnalyzer
from error_handling import get_logger, with_error_context
from skillicon_mapper import SkilliconMapper

logger = get_logger(__name__)


class EnhancedDependencyAnalyzer:
    """Enhanced dependency analyzer that provides comprehensive tech stack analysis."""

    def __init__(self) -> None:
        """Initialize the enhanced dependency analyzer."""
        self.dependency_analyzer = DependencyAnalyzer()
        self.skillicon_mapper = SkilliconMapper()
        self.project_tech_mappings = self._load_project_tech_mappings()

    def _load_project_tech_mappings(self) -> dict[str, dict[str, list[str]]]:
        """Load technology mappings for known projects dynamically."""
        # Try to load from external configuration first
        config_file = Path(__file__).parent / "project_tech_mappings.json"
        if config_file.exists():
            try:
                with open(config_file, encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(
                    f"Failed to load project mappings from {config_file}: {e}"
                )

        # Fallback to hardcoded mappings (to be replaced with dynamic detection)
        return {
            "InmoIA Frontend": {
                "frontend": ["react", "ts", "js", "nextjs", "tailwind", "supabase"],
                "backend": [],
                "database": [],
                "devops": [],
                "ai_ml": [],
            },
            "TypeScript Backend": {
                "frontend": [],
                "backend": ["express", "jest", "nodejs", "prometheus", "redis", "ts"],
                "database": ["postgres"],
                "devops": ["docker"],
                "ai_ml": [],
            },
            "Python AI MCP Backend": {
                "frontend": [],
                "backend": ["py", "fastapi"],
                "database": ["postgres"],
                "devops": [],
                "ai_ml": ["openai", "langchain"],
            },
            "FacturaIA": {
                "frontend": ["react", "ts", "js"],
                "backend": ["py", "fastapi"],
                "database": ["postgres"],
                "devops": [],
                "ai_ml": ["opencv", "tesseract", "pandas", "numpy"],
            },
            "Restaurant App": {
                "frontend": ["react", "js"],
                "backend": ["nodejs", "express"],
                "database": ["mongodb"],
                "devops": [],
                "ai_ml": [],
            },
        }

    def _detect_technologies_from_description(
        self, description: str
    ) -> dict[str, list[str]]:
        """Extract technologies from project description using NLP/pattern matching."""
        detected_techs = {
            "frontend": [],
            "backend": [],
            "database": [],
            "devops": [],
            "ai_ml": [],
        }

        description_lower = description.lower()

        # Technology patterns for detection
        tech_patterns = {
            "frontend": {
                "react": ["react", "reactjs", "react.js"],
                "vue": ["vue", "vuejs", "vue.js"],
                "angular": ["angular", "angularjs"],
                "nextjs": ["next", "nextjs", "next.js"],
                "nuxt": ["nuxt", "nuxtjs", "nuxt.js"],
                "svelte": ["svelte", "sveltejs"],
                "typescript": ["typescript", "ts"],
                "javascript": ["javascript", "js", "es6", "es2015"],
                "tailwind": ["tailwind", "tailwindcss"],
                "bootstrap": ["bootstrap", "bootstrap 4", "bootstrap 5"],
                "css": ["css", "scss", "sass", "less"],
                "html": ["html", "html5"],
            },
            "backend": {
                "python": ["python", "py", "django", "flask", "fastapi"],
                "nodejs": ["node", "nodejs", "node.js", "express", "koa"],
                "java": ["java", "spring", "springboot"],
                "csharp": ["c#", "csharp", ".net", "asp.net"],
                "go": ["go", "golang"],
                "rust": ["rust"],
                "php": ["php", "laravel", "symfony"],
                "ruby": ["ruby", "rails", "sinatra"],
            },
            "database": {
                "postgres": ["postgres", "postgresql", "psql"],
                "mysql": ["mysql", "mariadb"],
                "mongodb": ["mongo", "mongodb"],
                "redis": ["redis"],
                "sqlite": ["sqlite"],
                "elasticsearch": ["elasticsearch", "elastic"],
                "dynamodb": ["dynamodb", "dynamo"],
            },
            "devops": {
                "docker": ["docker", "container"],
                "kubernetes": ["kubernetes", "k8s"],
                "aws": ["aws", "amazon", "ec2", "s3", "lambda"],
                "azure": ["azure", "microsoft"],
                "gcp": ["gcp", "google cloud", "firebase"],
                "terraform": ["terraform"],
                "ansible": ["ansible"],
                "jenkins": ["jenkins"],
                "github": ["github", "github actions"],
                "gitlab": ["gitlab", "gitlab ci"],
            },
            "ai_ml": {
                "tensorflow": ["tensorflow", "tf"],
                "pytorch": ["pytorch", "torch"],
                "sklearn": ["sklearn", "scikit-learn"],
                "opencv": ["opencv", "cv2"],
                "pandas": ["pandas", "pd"],
                "numpy": ["numpy", "np"],
                "openai": ["openai", "gpt", "chatgpt"],
                "anthropic": ["anthropic", "claude"],
                "langchain": ["langchain"],
                "transformers": ["transformers", "huggingface"],
            },
        }

        # Detect technologies from description
        for category, techs in tech_patterns.items():
            for tech_name, patterns in techs.items():
                for pattern in patterns:
                    if pattern in description_lower:
                        if tech_name not in detected_techs[category]:
                            detected_techs[category].append(tech_name)
                        break

        return detected_techs

    def _load_dynamic_project_mappings(self) -> dict[str, dict[str, list[str]]]:
        """Load project mappings dynamically from GitHub API and local analysis."""
        try:
            # Load config to get repository information
            config_path = Path(__file__).parent.parent / "config.yml"
            if not config_path.exists():
                logger.warning("config.yml not found, using fallback mappings")
                return self._load_project_tech_mappings()

            with open(config_path, encoding="utf-8") as f:
                config = yaml.safe_load(f)

            repositories = config.get("repositories", [])
            dynamic_mappings = {}

            for repo_config in repositories:
                repo_name = repo_config.get("name")
                display_name = repo_config.get("display_name", repo_name)
                organization = repo_config.get("organization")

                if not repo_name or not organization:
                    continue

                # Try to get repository description from GitHub API
                description = self._get_repository_description(organization, repo_name)

                if description:
                    # Extract technologies from description
                    techs = self._detect_technologies_from_description(description)
                    dynamic_mappings[display_name] = techs
                else:
                    # Fallback to hardcoded mappings for this project
                    fallback_mappings = self._load_project_tech_mappings()
                    if display_name in fallback_mappings:
                        dynamic_mappings[display_name] = fallback_mappings[display_name]

            return dynamic_mappings

        except Exception as e:
            logger.error(f"Error loading dynamic project mappings: {e}")
            return self._load_project_tech_mappings()

    def _get_repository_description(
        self, organization: str, repo_name: str
    ) -> str | None:
        """Get repository description from GitHub API."""
        try:
            # Try to use GitHub API to get repository information

            # Use environment token if available
            token = os.environ.get("GITHUB_TOKEN") or os.environ.get(
                "PERSONAL_GITHUB_TOKEN"
            )

            headers = {}
            if token:
                headers["Authorization"] = f"token {token}"

            url = f"https://api.github.com/repos/{organization}/{repo_name}"
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                description = data.get("description", "") or ""
                # Also check topics for additional technology hints
                topics = data.get("topics", [])
                if topics:
                    description += " " + " ".join(topics)
                return description if description.strip() else None
            else:
                logger.warning(
                    f"Failed to get description for {organization}/{repo_name}: {response.status_code}"
                )
                return None

        except Exception as e:
            logger.warning(
                f"Error getting repository description for {organization}/{repo_name}: {e}"
            )
            return None

    @with_error_context({"component": "enhanced_dependency_analyzer"})
    def analyze_current_repository(self) -> dict[str, set[str]]:
        """Analyze dependencies in the current repository."""
        try:
            current_dir = Path.cwd()
            return self.dependency_analyzer.analyze_repository_dependencies(current_dir)
        except Exception as e:
            logger.error(f"Error analyzing current repository: {e}")
            return {
                "frontend": set(),
                "backend": set(),
                "database": set(),
                "devops": set(),
                "ai_ml": set(),
            }

    @with_error_context({"component": "enhanced_dependency_analyzer"})
    def get_comprehensive_tech_stack(self) -> dict[str, Any]:
        """Generate comprehensive tech stack from all sources."""
        all_technologies: dict[str, set[str]] = {
            "frontend": set(),
            "backend": set(),
            "database": set(),
            "devops": set(),
            "ai_ml": set(),
        }

        # 1. Analyze current repository
        logger.info("Analyzing current repository...")
        current_tech = self.analyze_current_repository()
        for category, techs in current_tech.items():
            all_technologies[category].update(techs)

        # 2. Add technologies from known projects (dynamic detection)
        logger.info("Adding technologies from known projects...")
        dynamic_mappings = self._load_dynamic_project_mappings()
        for project_name, project_tech in dynamic_mappings.items():
            logger.info(f"Processing project: {project_name}")
            for category, techs in project_tech.items():
                # Convert list to set for proper update
                if isinstance(techs, list):
                    all_technologies[category].update(techs)
                elif isinstance(techs, set):
                    all_technologies[category].update(techs)
                else:
                    logger.warning(f"Unexpected tech format for {project_name}: {type(techs)}")

        # 3. Add dynamically detected common technologies
        logger.info("Adding dynamically detected common technologies...")
        dynamic_common_techs = self._detect_common_technologies_dynamically()
        for category, techs in dynamic_common_techs.items():
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

    def _detect_common_technologies_dynamically(self) -> dict[str, set[str]]:
        """Dynamically detect common technologies based on analysis patterns."""
        common_techs = {
            "frontend": set(),
            "backend": set(),
            "database": set(),
            "devops": set(),
            "ai_ml": set(),
        }

        try:
            # Analyze current repository structure for common patterns
            current_dir = Path.cwd()
            
            # Check for common development tools and patterns
            if (current_dir / "package.json").exists():
                common_techs["frontend"].add("html")
                common_techs["frontend"].add("css")
                common_techs["devops"].add("git")
                common_techs["devops"].add("github")
            
            if (current_dir / "requirements.txt").exists() or (current_dir / "pyproject.toml").exists():
                common_techs["backend"].add("python")
                common_techs["devops"].add("git")
                common_techs["devops"].add("github")
            
            if (current_dir / "Dockerfile").exists():
                common_techs["devops"].add("docker")
            
            if (current_dir / ".github").exists():
                common_techs["devops"].add("github")
                common_techs["devops"].add("githubactions")
            
            if (current_dir / "terraform").exists() or list(current_dir.glob("*.tf")):
                common_techs["devops"].add("terraform")
            
            # Check for common file patterns
            if list(current_dir.rglob("*.js")) or list(current_dir.rglob("*.ts")):
                common_techs["frontend"].add("javascript")
                common_techs["backend"].add("nodejs")
            
            if list(current_dir.rglob("*.py")):
                common_techs["backend"].add("python")
            
            if list(current_dir.rglob("*.ipynb")):
                common_techs["ai_ml"].add("jupyter")
                common_techs["ai_ml"].add("pandas")
                common_techs["ai_ml"].add("numpy")
            
            # Check for database files
            if list(current_dir.rglob("*.sql")) or list(current_dir.rglob("*.db")):
                common_techs["database"].add("sqlite")
            
            # Check for cloud configuration
            if list(current_dir.glob("*.yml")) or list(current_dir.glob("*.yaml")):
                yaml_files = list(current_dir.glob("*.yml")) + list(current_dir.glob("*.yaml"))
                for yaml_file in yaml_files:
                    try:
                        with open(yaml_file, 'r') as f:
                            content = f.read().lower()
                            if "aws" in content or "amazon" in content:
                                common_techs["devops"].add("aws")
                            if "azure" in content:
                                common_techs["devops"].add("azure")
                            if "gcp" in content or "google" in content:
                                common_techs["devops"].add("gcp")
                    except:
                        continue

        except Exception as e:
            logger.warning(f"Error in dynamic common technology detection: {e}")

        return common_techs

    @with_error_context({"component": "enhanced_dependency_analyzer"})
    def generate_enhanced_tech_stack(self) -> dict[str, Any]:
        """Generate enhanced tech stack and save to file."""
        try:
            # Generate comprehensive tech stack
            tech_stack = self.get_comprehensive_tech_stack()

            # Add metadata
            result = {
                "timestamp": self._get_timestamp(),
                "metadata": {
                    "version": "3.0",
                    "generated_by": "Enhanced Dependency Analyzer",
                    "data_source": "Multi-Source Technology Analysis",
                },
                "tech_stack_analysis": tech_stack,
                "project_count": len(self.project_tech_mappings),
                "total_technologies": sum(
                    len(data.get("technologies", [])) for data in tech_stack.values()
                ),
                "analysis_methods": [
                    "Current repository dependency analysis",
                    "Known project technology mapping",
                    "Common technology inclusion",
                ],
            }

            # Save to file
            output_file = Path(__file__).parent.parent / "enhanced_tech_stack.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            logger.info(f"Enhanced tech stack saved to {output_file}")
            return result

        except Exception as e:
            logger.error(f"Failed to generate enhanced tech stack: {e}")
            return {}

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.utcnow().isoformat() + "Z"


def main() -> None:
    """Main function to generate enhanced tech stack."""
    analyzer = EnhancedDependencyAnalyzer()
    result = analyzer.generate_enhanced_tech_stack()

    if result:
        print("✅ Enhanced tech stack generated successfully!")
        print(
            f"📊 Found {result.get('total_technologies', 0)} technologies from {result.get('project_count', 0)} projects"
        )

        tech_stack = result.get("tech_stack_analysis", {})
        for category, data in tech_stack.items():
            techs = data.get("technologies", [])
            if techs:
                print(
                    f"🔧 {category.title()}: {', '.join(techs[:5])}{'...' if len(techs) > 5 else ''}"
                )
    else:
        print("❌ Failed to generate enhanced tech stack")


if __name__ == "__main__":
    main()

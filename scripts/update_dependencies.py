#!/usr/bin/env python3
"""
Enhanced Dependency Management Script
Handles version pinning, security updates, missing dependencies, and automatic dependency management.
"""

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from error_handling import DataProcessingError, get_logger, log_and_raise

# Set up logging for this module
logger = get_logger(__name__)


@dataclass
class PackageInfo:
    """Represents package information."""

    name: str
    current_version: str
    latest_version: str
    version_spec: str
    is_security_update: bool
    is_major_update: bool
    is_optional: bool
    used_in_code: bool


@dataclass
class DependencyReport:
    """Represents a dependency analysis report."""

    total_packages: int
    up_to_date: int
    updates_available: int
    security_updates: int
    major_updates: int
    missing_dependencies: list[str]
    unused_dependencies: list[str]
    recommendations: list[str]


class DependencyManager:
    """Manages project dependencies with enhanced features."""

    def __init__(
        self,
        requirements_file: str = "requirements.txt",
        config_file: str = "dependency_config.yml",
    ):
        # Handle relative paths - requirements.txt should be in parent directory
        if not os.path.isabs(requirements_file):
            script_dir = Path(__file__).parent
            self.requirements_file = script_dir.parent / requirements_file
        else:
            self.requirements_file = Path(requirements_file)

        self.config_file = config_file
        self.logger = get_logger(__name__)

        # Load configuration
        self.config = self._load_config()

        # Define optional dependencies that might not be in requirements.txt
        self.optional_dependencies = self.config.get(
            "optional_dependencies",
            {
                "python-json-logger": "pythonjsonlogger",
                "svgwrite": "svgwrite",
                "requests": "requests",
                "PyYAML": "yaml",
                "colorama": "colorama",
                "tqdm": "tqdm",
                "git-fame": "git_fame",
            },
        )

        # Define security-critical packages
        self.security_critical = set(
            self.config.get(
                "security_critical_packages",
                ["requests", "PyYAML", "urllib3", "cryptography", "ssl"],
            )
        )

        # Define packages that should be pinned to exact versions
        self.pin_exact_versions = set(
            self.config.get(
                "pin_exact_versions",
                [
                    "requests",
                    "PyYAML",
                    "cryptography",
                    "ruff",
                    "black",
                    "mypy",
                    "safety",
                ],
            )
        )

        # Define excluded packages
        self.excluded_packages = set(
            self.config.get("excluded_packages", ["setuptools", "pip", "wheel"])
        )

        # Update strategies
        self.update_strategies = self.config.get(
            "update_strategies",
            {"security": "auto", "major": "manual", "minor": "auto", "patch": "auto"},
        )

    def _load_config(self) -> dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            import yaml

            config_path = Path(__file__).parent / self.config_file

            if not config_path.exists():
                self.logger.warning(
                    f"Configuration file not found: {config_path}, using defaults"
                )
                return {}

            with open(config_path, encoding="utf-8") as f:
                config = yaml.safe_load(f)

            self.logger.debug(f"Loaded configuration from {config_path}")
            return config or {}

        except Exception as e:
            self.logger.warning(f"Error loading configuration: {e}, using defaults")
            return {}

    def run_command(self, cmd: list[str], timeout: int = 30) -> tuple[int, str, str]:
        """Run a command with enhanced error handling."""
        try:
            # nosec B603: cmd is validated and contains trusted pip commands
            result = subprocess.run(  # nosec B603
                cmd, capture_output=True, text=True, timeout=timeout, check=False
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            self.logger.warning(f"Command timed out: {' '.join(cmd)}")
            return -1, "", "Command timed out"
        except Exception as e:
            self.logger.error(f"Command failed: {' '.join(cmd)} - {e}")
            return -1, "", str(e)

    def get_latest_version(self, package_name: str) -> str | None:
        """Get the latest version of a package with enhanced error handling."""
        try:
            # Try pip index first with better parsing
            cmd = ["pip", "index", "versions", package_name]
            return_code, stdout, stderr = self.run_command(cmd)

            if return_code == 0:
                # Parse the output to find the latest version
                lines = stdout.split("\n")
                for line in lines:
                    if "LATEST:" in line:
                        version = line.split("LATEST:")[1].strip()
                        if version and version != "999.999.999":
                            return version
                    # Also check for version in parentheses
                    elif "(" in line and ")" in line:
                        match = re.search(r"\(([0-9]+\.[0-9]+(?:\.[0-9]+)?)\)", line)
                        if match:
                            version = match.group(1)
                            if version and version != "999.999.999":
                                return version

            # Fallback: try pip install with --dry-run and better parsing
            cmd = ["pip", "install", f"{package_name}==999.999.999", "--dry-run"]
            return_code, stdout, stderr = self.run_command(cmd)

            if return_code != 0:
                # Extract version from error message - try multiple patterns
                patterns = [
                    r"ERROR: No matching distribution found for ([^=]+)==([0-9.]+)",
                ]

                for pattern in patterns:
                    match = re.search(pattern, stderr)
                    if match:
                        version = match.group(2)
                        if version and version != "999.999.999":
                            return version

            # Additional fallback: try pip show for installed packages
            cmd = ["pip", "show", package_name]
            return_code, stdout, stderr = self.run_command(cmd)

            if return_code == 0:
                # Look for version in pip show output
                for line in stdout.split("\n"):
                    if line.startswith("Version:"):
                        version = line.split(":", 1)[1].strip()
                        if version and version != "999.999.999":
                            return version

            # If we still don't have a valid version, return None
            self.logger.warning(
                f"Could not determine latest version for {package_name}"
            )
            return None

        except Exception as e:
            self.logger.error(f"Error getting latest version for {package_name}: {e}")
            return None

    def get_security_info(self, package_name: str, version: str) -> dict[str, Any]:
        """Get security information for a package version."""
        try:
            # This would integrate with security databases like NVD
            # For now, return basic info
            return {
                "has_vulnerabilities": False,
                "last_checked": datetime.now().isoformat(),
                "recommendation": "up_to_date",
            }
        except Exception as e:
            self.logger.warning(f"Could not get security info for {package_name}: {e}")
            return {
                "has_vulnerabilities": False,
                "last_checked": None,
                "recommendation": "unknown",
            }

    def parse_requirements_file(self) -> list[tuple[str, str]]:
        """Parse requirements.txt with enhanced error handling."""
        requirements = []

        try:
            if not self.requirements_file.exists():
                self.logger.warning(
                    f"Requirements file not found: {self.requirements_file}"
                )
                return []

            with open(self.requirements_file, encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Parse package name and version spec
                        match = re.match(r"^([a-zA-Z0-9_-]+)(.*)$", line)
                        if match:
                            package = match.group(1)
                            version_spec = match.group(2).strip()
                            requirements.append((package, version_spec))
                        else:
                            self.logger.warning(
                                f"Invalid requirement format at line {line_num}: {line}"
                            )

        except Exception as e:
            log_and_raise(
                DataProcessingError(
                    f"Error parsing requirements file {self.requirements_file}: {e}",
                    context={"file": self.requirements_file, "error": str(e)},
                ),
                logger=self.logger,
            )

        return requirements

    def scan_code_for_imports(self) -> set[str]:
        """Scan Python files for import statements to find used dependencies."""
        used_packages = set()
        scripts_dir = Path(__file__).parent

        try:
            for py_file in scripts_dir.rglob("*.py"):
                if py_file.name == "__pycache__":
                    continue

                with open(py_file, encoding="utf-8") as f:
                    content = f.read()

                    # Find import statements
                    import_patterns = [
                        r"import\s+([a-zA-Z_][a-zA-Z0-9_]*)",
                        r"from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+import",
                        r"from\s+([a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*)\s+import",
                    ]

                    for pattern in import_patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            # Extract the base package name
                            base_package = match.split(".")[0]
                            used_packages.add(base_package)

        except Exception as e:
            self.logger.warning(f"Error scanning code for imports: {e}")

        return used_packages

    def check_current_versions(
        self, requirements: list[tuple[str, str]]
    ) -> dict[str, str]:
        """Check current installed versions with enhanced error handling."""
        current_versions = {}

        for package, _ in requirements:
            try:
                cmd = ["pip", "show", package]
                return_code, stdout, stderr = self.run_command(cmd)

                if return_code == 0:
                    # Parse version from pip show output
                    for line in stdout.split("\n"):
                        if line.startswith("Version:"):
                            version = line.split("Version:")[1].strip()
                            current_versions[package] = version
                            break
                    else:
                        current_versions[package] = "Not found"
                else:
                    current_versions[package] = "Not installed"

            except Exception as e:
                self.logger.warning(f"Error checking version for {package}: {e}")
                current_versions[package] = "Error"

        return current_versions

    def analyze_dependencies(self) -> DependencyReport:
        """Perform comprehensive dependency analysis."""
        self.logger.info("Starting comprehensive dependency analysis")

        # Parse requirements
        requirements = self.parse_requirements_file()
        if not requirements:
            return DependencyReport(
                total_packages=0,
                up_to_date=0,
                updates_available=0,
                security_updates=0,
                major_updates=0,
                missing_dependencies=[],
                unused_dependencies=[],
                recommendations=[],
            )

        # Check current versions
        current_versions = self.check_current_versions(requirements)

        # Scan code for imports
        used_packages = self.scan_code_for_imports()

        # Analyze each package
        packages_info = []
        updates_available = 0
        security_updates = 0
        major_updates = 0
        missing_dependencies = []
        unused_dependencies = []

        for package, version_spec in requirements:
            # Skip excluded packages
            if package in self.excluded_packages:
                self.logger.debug(f"Skipping excluded package: {package}")
                continue

            current_version = current_versions.get(package, "Unknown")
            latest_version = self.get_latest_version(package)

            if not latest_version:
                self.logger.warning(f"Could not determine latest version for {package}")
                continue

            # Check if update is needed
            needs_update = current_version != latest_version

            # Determine update type
            is_security_update = package in self.security_critical and needs_update
            is_major_update = self._is_major_version_update(
                current_version, latest_version
            )
            is_optional = package in self.optional_dependencies
            # Check if package is used in code (including optional dependency mappings)
            used_in_code = (
                package in used_packages
                or package in self.optional_dependencies.values()
                or any(
                    pkg in used_packages
                    for pkg in self.optional_dependencies.get(package, [])
                )
            )

            if needs_update:
                updates_available += 1
                if is_security_update:
                    security_updates += 1
                if is_major_update:
                    major_updates += 1

            if not used_in_code and not is_optional:
                unused_dependencies.append(package)

            packages_info.append(
                PackageInfo(
                    name=package,
                    current_version=current_version,
                    latest_version=latest_version,
                    version_spec=version_spec,
                    is_security_update=is_security_update,
                    is_major_update=is_major_update,
                    is_optional=is_optional,
                    used_in_code=used_in_code,
                )
            )

        # Check for missing dependencies (filter out standard library and internal modules)
        standard_library_modules = {
            "os",
            "sys",
            "json",
            "re",
            "math",
            "datetime",
            "pathlib",
            "subprocess",
            "typing",
            "dataclasses",
            "logging",
            "traceback",
            "statistics",
            "dataclass",
            "Optional",
            "Dict",
            "List",
            "Path",
            "Tuple",
            "Set",
            "Any",
            "Union",
            "Callable",
            "Iterator",
            "Generator",
            "AsyncGenerator",
        }

        internal_modules = {
            "error_handling",
            "config_manager",
            "stats_processor",
            "language_mapper",
            "git_fame_parser",
            "dependency_analyzer",
            "analytics_manager",
            "analytics_reporter",
            "report_generator",
            "update_dependencies",
            "DependencyManager",
            "PackageInfo",
            "DependencyReport",
            "get_logger",
            "setup_logging",
            "create_config_manager",
            "get_language_mapper",
            "get_analytics_manager",
            "get_analytics_reporter",
            "DataProcessingError",
            "StatsProcessingError",
            "LanguageMappingError",
            "SvgGenerationError",
            "AnalyticsError",
            "GitFameParser",
            "StatsProcessor",
            "AuthorMatcher",
            "UnifiedStats",
            "AuthorStats",
            "RotatingFileHandler",
            "MarkdownReportGenerator",
            "DependencyAnalyzer",
            "scanning",
            "statements",
            "jsonlogger",
        }

        for package in used_packages:
            # Skip standard library and internal modules
            if package in standard_library_modules or package in internal_modules:
                continue

            # Check if it's a valid external package
            if not any(pkg.name == package for pkg in packages_info):
                # Additional check: see if it's an optional dependency
                is_optional = any(
                    pkg == package for pkg in self.optional_dependencies.values()
                )
                if not is_optional:
                    missing_dependencies.append(package)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            packages_info, missing_dependencies, unused_dependencies
        )

        return DependencyReport(
            total_packages=len(requirements),
            up_to_date=len(requirements) - updates_available,
            updates_available=updates_available,
            security_updates=security_updates,
            major_updates=major_updates,
            missing_dependencies=missing_dependencies,
            unused_dependencies=unused_dependencies,
            recommendations=recommendations,
        )

    def _is_major_version_update(self, current: str, latest: str) -> bool:
        """Check if this is a major version update."""
        try:
            current_parts = current.split(".")
            latest_parts = latest.split(".")

            if len(current_parts) > 0 and len(latest_parts) > 0:
                current_major = int(current_parts[0])
                latest_major = int(latest_parts[0])
                return latest_major > current_major
        except (ValueError, IndexError):
            pass
        return False

    def _generate_recommendations(
        self,
        packages_info: list[PackageInfo],
        missing_deps: list[str],
        unused_deps: list[str],
    ) -> list[str]:
        """Generate recommendations based on analysis."""
        recommendations = []

        # Security updates
        security_packages = [pkg for pkg in packages_info if pkg.is_security_update]
        if security_packages:
            recommendations.append(
                f"🔒 Security updates available for: {', '.join(pkg.name for pkg in security_packages)}"
            )

        # Major updates
        major_packages = [pkg for pkg in packages_info if pkg.is_major_update]
        if major_packages:
            recommendations.append(
                f"⚠️ Major version updates available for: {', '.join(pkg.name for pkg in major_packages)}"
            )

        # Missing dependencies
        if missing_deps:
            recommendations.append(
                f"➕ Missing dependencies detected: {', '.join(missing_deps)}"
            )

        # Unused dependencies
        if unused_deps:
            recommendations.append(f"🗑️ Unused dependencies: {', '.join(unused_deps)}")

        # Version pinning
        unpinned_packages = [
            pkg
            for pkg in packages_info
            if ">=" in pkg.version_spec and pkg.name in self.pin_exact_versions
        ]
        if unpinned_packages:
            recommendations.append(
                f"📌 Consider pinning exact versions for: {', '.join(pkg.name for pkg in unpinned_packages)}"
            )

        return recommendations

    def update_requirements_file(
        self, packages_info: list[PackageInfo], pin_versions: bool = False
    ) -> bool:
        """Update requirements.txt with new versions."""
        try:
            with open(self.requirements_file, encoding="utf-8") as f:
                content = f.read()

            # Update each package version
            for package_info in packages_info:
                if package_info.current_version != package_info.latest_version:
                    # Determine new version spec
                    if pin_versions or package_info.name in self.pin_exact_versions:
                        new_spec = f"{package_info.name}=={package_info.latest_version}"
                    else:
                        new_spec = f"{package_info.name}>={package_info.latest_version}"

                    # Find and replace the version specification
                    pattern = rf"^{package_info.name}.*$"
                    replacement = new_spec
                    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

            # Write back to file
            with open(self.requirements_file, "w", encoding="utf-8") as f:
                f.write(content)

            self.logger.info(f"Successfully updated {self.requirements_file}")
            return True

        except Exception as e:
            log_and_raise(
                DataProcessingError(
                    f"Error updating requirements file: {e}",
                    context={"file": self.requirements_file, "error": str(e)},
                ),
                logger=self.logger,
            )
            return False  # This line will never be reached due to log_and_raise

    def generate_dependency_report(
        self, report: DependencyReport, packages_info: list[PackageInfo]
    ) -> str:
        """Generate a comprehensive dependency report."""
        report_lines = []
        report_lines.append("# 📊 Dependency Analysis Report")
        report_lines.append(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        report_lines.append("")

        # Summary
        report_lines.append("## 📈 Summary")
        report_lines.append(f"- **Total Packages**: {report.total_packages}")
        report_lines.append(f"- **Up to Date**: {report.up_to_date}")
        report_lines.append(f"- **Updates Available**: {report.updates_available}")
        report_lines.append(f"- **Security Updates**: {report.security_updates}")
        report_lines.append(f"- **Major Updates**: {report.major_updates}")
        report_lines.append("")

        # Package details
        report_lines.append("## 📦 Package Details")
        for package_info in packages_info:
            status = (
                "✅"
                if package_info.current_version == package_info.latest_version
                else "🔄"
            )
            security_icon = "🔒" if package_info.is_security_update else ""
            major_icon = "⚠️" if package_info.is_major_update else ""

            report_lines.append(f"### {package_info.name}")
            report_lines.append(f"- **Current**: {package_info.current_version}")
            report_lines.append(f"- **Latest**: {package_info.latest_version}")
            report_lines.append(f"- **Status**: {status} {security_icon} {major_icon}")
            report_lines.append(
                f"- **Used in Code**: {'Yes' if package_info.used_in_code else 'No'}"
            )
            report_lines.append("")

        # Issues
        if report.missing_dependencies:
            report_lines.append("## ❌ Missing Dependencies")
            for dep in report.missing_dependencies:
                report_lines.append(f"- {dep}")
            report_lines.append("")

        if report.unused_dependencies:
            report_lines.append("## 🗑️ Unused Dependencies")
            for dep in report.unused_dependencies:
                report_lines.append(f"- {dep}")
            report_lines.append("")

        # Recommendations
        if report.recommendations:
            report_lines.append("## 💡 Recommendations")
            for rec in report.recommendations:
                report_lines.append(f"- {rec}")
            report_lines.append("")

        return "\n".join(report_lines)


def main() -> None:
    """Main function with enhanced dependency management."""
    logger.info("🔧 Enhanced Dependency Management Script")
    logger.info("=" * 60)

    try:
        # Initialize dependency manager
        manager = DependencyManager()

        # Perform comprehensive analysis
        logger.info("\n🔍 Performing comprehensive dependency analysis...")
        report = manager.analyze_dependencies()

        # Get packages info for the report
        requirements = manager.parse_requirements_file()
        if not requirements:
            logger.error(
                "❌ No requirements found. Please check if requirements.txt exists and contains valid packages."
            )
            return

        current_versions = manager.check_current_versions(requirements)
        used_packages = manager.scan_code_for_imports()

        packages_info = []
        for package, version_spec in requirements:
            if package in manager.excluded_packages:
                continue

            current_version = current_versions.get(package, "Unknown")
            latest_version = manager.get_latest_version(package)

            if not latest_version:
                continue

            needs_update = current_version != latest_version
            is_security_update = package in manager.security_critical and needs_update
            is_major_update = manager._is_major_version_update(
                current_version, latest_version
            )
            is_optional = package in manager.optional_dependencies
            used_in_code = package in used_packages or any(
                pkg in used_packages
                for pkg in manager.optional_dependencies.get(package, [])
            )

            packages_info.append(
                PackageInfo(
                    name=package,
                    current_version=current_version,
                    latest_version=latest_version,
                    version_spec=version_spec,
                    is_security_update=is_security_update,
                    is_major_update=is_major_update,
                    is_optional=is_optional,
                    used_in_code=used_in_code,
                )
            )

        # Display summary
        logger.info("\n📊 Analysis Summary:")
        logger.info(f"  Total packages: {report.total_packages}")
        logger.info(f"  Up to date: {report.up_to_date}")
        logger.info(f"  Updates available: {report.updates_available}")
        logger.info(f"  Security updates: {report.security_updates}")
        logger.info(f"  Major updates: {report.major_updates}")

        if report.missing_dependencies:
            logger.info(f"  Missing dependencies: {len(report.missing_dependencies)}")

        if report.unused_dependencies:
            logger.info(f"  Unused dependencies: {len(report.unused_dependencies)}")

        # Show recommendations
        if report.recommendations:
            logger.info("\n💡 Recommendations:")
            for rec in report.recommendations:
                logger.info(f"  {rec}")

        # Ask for action (handle non-interactive environments)
        if report.updates_available > 0:
            logger.info(f"\n🔄 {report.updates_available} updates available")

            if report.security_updates > 0:
                logger.info(
                    f"🔒 {report.security_updates} security updates - RECOMMENDED"
                )

            # Check if we're in an interactive environment
            try:
                # Try to get input, but handle non-interactive environments gracefully
                response = (
                    input("\n❓ Update dependencies? (y/N/p for pin exact versions): ")
                    .strip()
                    .lower()
                )

                if response in ["y", "yes"]:
                    # Update with >= versions
                    if manager.update_requirements_file(
                        packages_info, pin_versions=False
                    ):
                        logger.info("✅ Successfully updated requirements.txt")
                    else:
                        logger.error("❌ Failed to update requirements.txt")

                elif response == "p":
                    # Update with == versions (pinned)
                    if manager.update_requirements_file(
                        packages_info, pin_versions=True
                    ):
                        logger.info(
                            "✅ Successfully updated requirements.txt with pinned versions"
                        )
                    else:
                        logger.error("❌ Failed to update requirements.txt")
                else:
                    logger.info("ℹ️ No changes made")
            except EOFError:
                # Non-interactive environment (like GitHub Actions)
                logger.info(
                    "ℹ️ Non-interactive environment detected - no automatic updates"
                )
                logger.info(
                    "ℹ️ Run manually with interactive input to update dependencies"
                )
            except Exception as e:
                logger.warning(f"⚠️ Error reading input: {e}")
                logger.info("ℹ️ No changes made")

        # Generate and save report
        report_content = manager.generate_dependency_report(report, packages_info)

        # Save report in both locations for compatibility
        report_files = [
            Path(__file__).parent.parent / "dependency_report.md",  # Project root
            Path(__file__).parent / "dependency_report.md",  # Scripts directory
        ]

        for report_file in report_files:
            try:
                with open(report_file, "w", encoding="utf-8") as f:
                    f.write(report_content)
                logger.info(f"\n📄 Detailed report saved to: {report_file}")
                break  # Successfully saved, no need to try other locations
            except Exception as e:
                logger.warning(f"⚠️ Could not save report to {report_file}: {e}")
                continue

        logger.info("\n🎉 Dependency analysis completed!")

    except Exception as e:
        logger.error(f"Error in dependency management: {e}")
        logger.error(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

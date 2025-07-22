#!/usr/bin/env python3
"""
Update Tech Stack
Updates the tech stack analysis and regenerates the README with the latest data.
Uses both enhanced and API-based analyzers for comprehensive coverage.
"""

import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from api_based_repository_analyzer import APIBasedRepositoryAnalyzer  # noqa: E402
from enhanced_dependency_analyzer import EnhancedDependencyAnalyzer  # noqa: E402
from enhanced_readme_generator import main as generate_readme  # noqa: E402
from error_handling import get_logger  # noqa: E402

logger = get_logger(__name__)


def main() -> None:
    """Update tech stack and regenerate README using both analyzers."""
    try:
        print("🚀 Starting comprehensive tech stack analysis...")

        # Strategy: Try API-based first, fallback to enhanced
        api_result = None
        enhanced_result = None

        # 1. Try API-based analyzer (most comprehensive)
        print("\n📡 Attempting API-based repository analysis...")
        try:
            api_analyzer = APIBasedRepositoryAnalyzer()
            api_result = api_analyzer.generate_api_based_tech_stack()

            if api_result and api_result.get("total_technologies", 0) > 0:
                print("✅ API-based analysis successful!")
                print(
                    f"📊 Found {api_result.get('total_technologies', 0)} technologies across {api_result.get('repository_count', 0)} repositories"
                )

                tech_stack = api_result.get("tech_stack_analysis", {})
                for category, data in tech_stack.items():
                    techs = data.get("technologies", [])
                    if techs:
                        print(
                            f"🔧 {category.title()}: {', '.join(techs[:5])}{'...' if len(techs) > 5 else ''}"
                        )
            else:
                print(
                    "⚠️ API-based analysis found no technologies, trying enhanced analyzer..."
                )
                api_result = None

        except Exception as e:
            logger.warning(f"API-based analysis failed: {e}")
            print("⚠️ API-based analysis failed, falling back to enhanced analyzer...")
            api_result = None

        # 2. Fallback to enhanced analyzer
        if not api_result:
            print("\n🔧 Using enhanced dependency analyzer...")
            try:
                enhanced_analyzer = EnhancedDependencyAnalyzer()
                enhanced_result = enhanced_analyzer.generate_enhanced_tech_stack()

                if enhanced_result:
                    print("✅ Enhanced tech stack generated successfully!")
                    print(
                        f"📊 Found {enhanced_result.get('total_technologies', 0)} technologies from {enhanced_result.get('project_count', 0)} projects"
                    )

                    tech_stack = enhanced_result.get("tech_stack_analysis", {})
                    for category, data in tech_stack.items():
                        techs = data.get("technologies", [])
                        if techs:
                            print(
                                f"🔧 {category.title()}: {', '.join(techs[:5])}{'...' if len(techs) > 5 else ''}"
                            )
                else:
                    print("❌ Enhanced analyzer also failed")
                    sys.exit(1)

            except Exception as e:
                logger.error(f"Enhanced analyzer failed: {e}")
                print("❌ Both analyzers failed")
                sys.exit(1)

        # 3. Regenerate README
        print("\n🔄 Regenerating README with updated tech stack...")
        generate_readme()

        # 4. Summary
        print("✅ README updated successfully!")
        print("\n🎉 Tech stack analysis complete!")

        if api_result:
            print("📊 Analysis method: API-based repository analysis")
            print("   • GitHub API repository analysis")
            print("   • Dependency file content analysis")
            print("   • Repository structure detection")
            print("   • Description and topics analysis")
        else:
            print("📊 Analysis method: Enhanced dependency analysis")
            print("   • Current repository dependency analysis")
            print("   • Known project technology mapping")
            print("   • Dynamic common technology detection")

        print(
            f"\n💡 Total technologies found: {api_result.get('total_technologies', 0) if api_result else enhanced_result.get('total_technologies', 0)}"
        )

    except Exception as e:
        logger.error(f"Error updating tech stack: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

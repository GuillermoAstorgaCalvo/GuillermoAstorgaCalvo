#!/usr/bin/env python3
"""
Test script for dynamic project tech stack detection
"""

import sys
from pathlib import Path


def setup_path():
    """Add scripts directory to path for imports"""
    scripts_dir = Path(__file__).parent
    sys.path.insert(0, str(scripts_dir))


def main():
    # Setup path for local imports
    setup_path()

    # Import after path setup
    from api_based_repository_analyzer import APIBasedRepositoryAnalyzer
    from enhanced_readme_generator import (
        _get_base_project_descriptions,
        get_dynamic_project_descriptions,
    )

    print("🧪 Testing Dynamic Project Tech Stack Detection")
    print("=" * 50)

    # Test API-based analysis
    print("\n1. Testing API-based repository analysis...")
    try:
        analyzer = APIBasedRepositoryAnalyzer()
        api_result = analyzer.analyze_all_repositories()
        print("✅ API Analysis successful")
        print(f"   Found categories: {list(api_result.keys())}")

        for category, data in api_result.items():
            techs = data.get("technologies", [])
            print(f"   {category}: {techs}")

    except Exception as e:
        print(f"❌ API Analysis failed: {e}")
        api_result = None

    # Test dynamic project descriptions
    print("\n2. Testing dynamic project descriptions...")
    try:
        dynamic_projects = get_dynamic_project_descriptions()
        print("✅ Dynamic project analysis successful")

        for project_name, project_info in dynamic_projects.items():
            tech_stack = project_info.get("tech_stack", [])
            print(f"   {project_name}: {tech_stack}")

    except Exception as e:
        print(f"❌ Dynamic project analysis failed: {e}")

    # Test base project descriptions
    print("\n3. Testing base project descriptions...")
    try:
        base_projects = _get_base_project_descriptions()
        print("✅ Base project descriptions loaded")

        for project_name, project_info in base_projects.items():
            tech_stack = project_info.get("tech_stack", [])
            print(f"   {project_name}: {tech_stack}")

    except Exception as e:
        print(f"❌ Base project descriptions failed: {e}")


if __name__ == "__main__":
    main()

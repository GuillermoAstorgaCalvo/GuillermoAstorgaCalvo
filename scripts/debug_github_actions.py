#!/usr/bin/env python3
"""
Debug script specifically for GitHub Actions environment
"""

import json
import os
from pathlib import Path
from dependency_analyzer import DependencyAnalyzer

def debug_github_actions_environment():
    """Debug the GitHub Actions environment for dependency analysis"""
    print("🔍 GitHub Actions Environment Debug")
    print("=" * 50)
    
    # Check environment variables
    print("📋 Environment Variables:")
    print(f"  REPO_NAME: {os.environ.get('REPO_NAME', 'NOT SET')}")
    print(f"  DISPLAY_NAME: {os.environ.get('DISPLAY_NAME', 'NOT SET')}")
    print(f"  GITHUB_WORKSPACE: {os.environ.get('GITHUB_WORKSPACE', 'NOT SET')}")
    print(f"  PWD: {os.getcwd()}")
    
    # Check repository directory
    repo_path = Path("../repo")
    print(f"\n📁 Repository Directory Check:")
    print(f"  Expected repo path: {repo_path.absolute()}")
    print(f"  Repo exists: {repo_path.exists()}")
    
    if repo_path.exists():
        print(f"  Repo is directory: {repo_path.is_dir()}")
        print(f"  Repo contents:")
        try:
            for item in repo_path.iterdir():
                print(f"    - {item.name} ({'dir' if item.is_dir() else 'file'})")
        except Exception as e:
            print(f"    ❌ Error listing contents: {e}")
    
    # Check for dependency files
    print(f"\n📦 Dependency Files Check:")
    if repo_path.exists():
        # Look for package.json files
        package_files = list(repo_path.rglob('package.json'))
        print(f"  package.json files found: {len(package_files)}")
        for pkg_file in package_files:
            print(f"    - {pkg_file.relative_to(repo_path)}")
            try:
                with open(pkg_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                deps = data.get('dependencies', {})
                dev_deps = data.get('devDependencies', {})
                print(f"      Dependencies: {len(deps)}")
                print(f"      DevDependencies: {len(dev_deps)}")
            except Exception as e:
                print(f"      ❌ Error reading package.json: {e}")
        
        # Look for requirements.txt files
        req_files = list(repo_path.rglob('requirements.txt'))
        print(f"  requirements.txt files found: {len(req_files)}")
        for req_file in req_files:
            print(f"    - {req_file.relative_to(repo_path)}")
            try:
                with open(req_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                print(f"      Lines: {len(lines)}")
            except Exception as e:
                print(f"      ❌ Error reading requirements.txt: {e}")
    
    # Test dependency analyzer
    print(f"\n🧪 Testing Dependency Analyzer:")
    if repo_path.exists():
        try:
            analyzer = DependencyAnalyzer()
            print("  ✅ DependencyAnalyzer initialized")
            
            tech_stack = analyzer.analyze_repository_dependencies(repo_path)
            print("  ✅ analyze_repository_dependencies completed")
            
            # Convert to serializable format
            tech_stack_serializable = {}
            for category, techs in tech_stack.items():
                tech_list = sorted(list(techs))
                tech_stack_serializable[category] = {
                    'technologies': tech_list,
                    'count': len(tech_list)
                }
            
            print("  ✅ Format conversion completed")
            
            # Test JSON serialization
            try:
                with open('debug_github_actions_tech_stack.json', 'w', encoding='utf-8') as f:
                    json.dump(tech_stack_serializable, f, indent=2, ensure_ascii=False)
                print("  ✅ JSON serialization successful")
                
                print("\n📊 Extracted Technologies:")
                for category, data in tech_stack_serializable.items():
                    if data['technologies']:
                        print(f"  {category.upper()}: {data['count']} technologies")
                        for tech in data['technologies'][:3]:  # Show first 3
                            print(f"    • {tech}")
                        if len(data['technologies']) > 3:
                            print(f"    ... and {len(data['technologies']) - 3} more")
                    else:
                        print(f"  {category.upper()}: No technologies detected")
                
            except Exception as e:
                print(f"  ❌ JSON serialization failed: {e}")
                
        except Exception as e:
            print(f"  ❌ Dependency analyzer failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("  ❌ Repository directory not found - cannot test analyzer")
    
    # Check file permissions
    print(f"\n🔐 File Permissions Check:")
    if repo_path.exists():
        try:
            test_file = repo_path / "test_permissions.txt"
            with open(test_file, 'w') as f:
                f.write("test")
            print("  ✅ Write permission: OK")
            test_file.unlink()
        except Exception as e:
            print(f"  ❌ Write permission failed: {e}")
    
    print("\n✅ GitHub Actions debug complete!")

if __name__ == "__main__":
    debug_github_actions_environment() 
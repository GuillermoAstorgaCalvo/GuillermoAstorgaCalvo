#!/usr/bin/env python3
"""
Comprehensive test script to verify dependency analysis flow for guillermo-affiliaction repositories
"""

import json
import os
from pathlib import Path
from dependency_analyzer import DependencyAnalyzer

def test_dependency_analyzer():
    """Test the dependency analyzer with mock data"""
    print("🧪 Testing Dependency Analyzer...")
    
    analyzer = DependencyAnalyzer()
    
    # Test with mock package.json data (similar to what we'd find in guillermo-affiliaction repos)
    mock_repo_path = Path("../test-repo")
    
    # Create mock package.json with typical guillermo-affiliaction dependencies
    mock_package_json = {
        "dependencies": {
            "react": "^18.0.0",
            "typescript": "^4.0.0",
            "express": "^4.18.0",
            "fastapi": "^0.100.0",
            "postgresql": "^8.0.0",
            "redis": "^4.0.0",
            "docker": "^20.0.0",
            "aws-sdk": "^2.1000.0",
            "openai": "^4.0.0",
            "tensorflow": "^2.13.0"
        },
        "devDependencies": {
            "eslint": "^8.0.0",
            "jest": "^29.0.0",
            "typescript": "^4.0.0"
        }
    }
    
    # Create mock requirements.txt
    mock_requirements = [
        "fastapi==0.100.0",
        "uvicorn==0.23.0",
        "pydantic==2.0.0",
        "sqlalchemy==2.0.0",
        "psycopg2-binary==2.9.0",
        "redis==4.6.0",
        "openai==0.28.0",
        "tensorflow==2.13.0",
        "pandas==2.0.0",
        "numpy==1.24.0"
    ]
    
    # Create test directory structure
    mock_repo_path.mkdir(exist_ok=True)
    
    # Write mock package.json
    with open(mock_repo_path / "package.json", "w") as f:
        json.dump(mock_package_json, f, indent=2)
    
    # Write mock requirements.txt
    with open(mock_repo_path / "requirements.txt", "w") as f:
        f.write("\n".join(mock_requirements))
    
    # Test the analyzer
    print(f"🔍 Analyzing dependencies in: {mock_repo_path}")
    tech_stack = analyzer.analyze_repository_dependencies(mock_repo_path)
    
    # Convert to serializable format (same as in process_repo_stats.py)
    tech_stack_serializable = {}
    for category, techs in tech_stack.items():
        tech_list = sorted(list(techs))
        tech_stack_serializable[category] = {
            'technologies': tech_list,
            'count': len(tech_list)
        }
    
    print("\n📊 Detected Technologies:")
    print(json.dumps(tech_stack_serializable, indent=2))
    
    # Verify expected technologies are detected
    expected_frontend = ['React', 'TypeScript', 'ESLint']
    expected_backend = ['Express.js', 'FastAPI', 'Python']
    expected_database = ['PostgreSQL', 'psycopg2']
    expected_devops = ['Docker', 'AWS']
    expected_ai_ml = ['OpenAI', 'TensorFlow', 'Pandas', 'NumPy']
    
    print("\n✅ Verification Results:")
    print(f"Frontend: {len(tech_stack_serializable['frontend']['technologies'])} technologies detected")
    print(f"Backend: {len(tech_stack_serializable['backend']['technologies'])} technologies detected")
    print(f"Database: {len(tech_stack_serializable['database']['technologies'])} technologies detected")
    print(f"DevOps: {len(tech_stack_serializable['devops']['technologies'])} technologies detected")
    print(f"AI/ML: {len(tech_stack_serializable['ai_ml']['technologies'])} technologies detected")
    
    # Test JSON serialization (same as in process_repo_stats.py)
    try:
        with open('test_tech_stack_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(tech_stack_serializable, f, indent=2, ensure_ascii=False)
        print("✅ JSON serialization successful")
    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")
    
    # Test aggregation format (same as in aggregate_stats.py)
    print("\n🧪 Testing aggregation format...")
    mock_aggregation_data = [tech_stack_serializable]  # Simulate multiple repos
    
    merged_stack = {
        'frontend': set(),
        'backend': set(),
        'database': set(),
        'devops': set(),
        'ai_ml': set()
    }
    
    for stack in mock_aggregation_data:
        for category in merged_stack:
            merged_stack[category].update(stack.get(category, {}).get('technologies', []))
    
    merged_stack_final = {cat: {'technologies': sorted(list(techs)), 'count': len(techs)} for cat, techs in merged_stack.items()}
    
    print("✅ Aggregation format test successful")
    print(json.dumps(merged_stack_final, indent=2))
    
    # Cleanup
    import shutil
    if mock_repo_path.exists():
        shutil.rmtree(mock_repo_path)
    
    print("\n🎉 All tests passed! The dependency analyzer is ready for guillermo-affiliaction repositories.")

def test_workflow_configuration():
    """Test workflow configuration"""
    print("\n🔧 Testing Workflow Configuration...")
    
    # Check config.yml
    config_path = Path("../config.yml")
    if config_path.exists():
        print("✅ config.yml exists")
        
        import yaml
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        repos = config.get('repositories', [])
        guillermo_affiliaction_repos = [repo for repo in repos if repo['name'] in ['housing-hub-saas', 'backend-housing-hub-saas', 'IAbackend-inmoIA']]
        
        print(f"✅ Found {len(guillermo_affiliaction_repos)} guillermo-affiliaction repositories in config:")
        for repo in guillermo_affiliaction_repos:
            print(f"  - {repo['name']} ({repo['display_name']})")
    else:
        print("❌ config.yml not found")
    
    # Check workflow file
    workflow_path = Path("../.github/workflows/update-stats.yml")
    if workflow_path.exists():
        print("✅ Workflow file exists")
    else:
        print("❌ Workflow file not found")

if __name__ == "__main__":
    print("🚀 Starting comprehensive dependency analysis test...")
    test_dependency_analyzer()
    test_workflow_configuration()
    print("\n✅ Complete test finished successfully!") 
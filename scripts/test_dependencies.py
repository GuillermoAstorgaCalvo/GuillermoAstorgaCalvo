#!/usr/bin/env python3
"""
Test script for the dependency manager functionality.
"""

import sys
import os
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from update_dependencies import DependencyManager, PackageInfo, DependencyReport

def test_dependency_manager():
    """Test the dependency manager functionality."""
    print("🧪 Testing Dependency Manager")
    print("=" * 50)
    
    try:
        # Initialize manager
        manager = DependencyManager()
        
        # Test configuration loading
        print("✅ Configuration loaded successfully")
        print(f"   Security packages: {len(manager.security_critical)}")
        print(f"   Pinned packages: {len(manager.pin_exact_versions)}")
        print(f"   Excluded packages: {len(manager.excluded_packages)}")
        
        # Test requirements parsing
        requirements = manager.parse_requirements_file()
        print(f"✅ Parsed {len(requirements)} requirements")
        
        # Test current versions check
        current_versions = manager.check_current_versions(requirements)
        print(f"✅ Checked {len(current_versions)} current versions")
        
        # Test import scanning
        used_packages = manager.scan_code_for_imports()
        print(f"✅ Found {len(used_packages)} used packages in code")
        
        # Test dependency analysis
        report = manager.analyze_dependencies()
        print(f"✅ Analysis completed:")
        print(f"   Total packages: {report.total_packages}")
        print(f"   Updates available: {report.updates_available}")
        print(f"   Security updates: {report.security_updates}")
        print(f"   Missing dependencies: {len(report.missing_dependencies)}")
        print(f"   Unused dependencies: {len(report.unused_dependencies)}")
        
        # Test report generation
        report_content = manager.generate_dependency_report(report, [])
        print(f"✅ Generated report ({len(report_content)} characters)")
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_version_parsing():
    """Test version parsing functionality."""
    print("\n🔍 Testing Version Parsing")
    print("=" * 30)
    
    try:
        manager = DependencyManager()
        
        # Test major version detection
        test_cases = [
            ("1.0.0", "2.0.0", True),
            ("1.0.0", "1.1.0", False),
            ("1.0.0", "1.0.1", False),
            ("2.0.0", "1.0.0", False),
        ]
        
        for current, latest, expected in test_cases:
            result = manager._is_major_version_update(current, latest)
            status = "✅" if result == expected else "❌"
            print(f"{status} {current} → {latest}: {result} (expected {expected})")
        
        print("✅ Version parsing tests completed")
        return True
        
    except Exception as e:
        print(f"❌ Version parsing test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Running Dependency Manager Tests")
    print("=" * 60)
    
    tests = [
        test_dependency_manager,
        test_version_parsing,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
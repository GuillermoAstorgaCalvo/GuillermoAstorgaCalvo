#!/usr/bin/env python3
"""
Manual README Regenerator
Quick script to regenerate README from current analytics data
"""

import os
import sys
import subprocess

def main():
    """Regenerate README from current analytics data"""
    print("🔄 Regenerating README from current analytics data...")
    
    # Change to scripts directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run the README generator
    try:
        result = subprocess.run([sys.executable, 'generate_readme.py'], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        print("✅ README regenerated successfully!")
        
        # Check if README was created in root
        readme_path = os.path.join(os.path.dirname(script_dir), 'README.md')
        if os.path.exists(readme_path):
            print(f"📄 README.md updated at: {readme_path}")
        else:
            print("⚠️  README.md not found in root directory")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error regenerating README: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
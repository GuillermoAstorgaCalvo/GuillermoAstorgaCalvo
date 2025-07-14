#!/usr/bin/env python3
"""
Debug script to show which technologies are extracted for each repository
"""

import json
import os
from pathlib import Path
from dependency_analyzer import DependencyAnalyzer

def debug_repository_technologies():
    """Debug technology extraction for each repository"""
    print("🔍 Debugging Technology Extraction for Each Repository")
    print("=" * 60)
    
    # Load config to get repository list
    config_path = Path("../config.yml")
    if not config_path.exists():
        print("❌ config.yml not found")
        return
    
    import yaml
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    repositories = config.get('repositories', [])
    
    print(f"📋 Found {len(repositories)} repositories to analyze:")
    for i, repo in enumerate(repositories, 1):
        print(f"  {i}. {repo['name']} ({repo['display_name']})")
    
    print("\n" + "=" * 60)
    
    # Test with mock data for each repository type
    analyzer = DependencyAnalyzer()
    
    # Mock data for different repository types
    mock_repos = {
        "housing-hub-saas": {
            "type": "Frontend React/TypeScript",
            "package.json": {
                "dependencies": {
                    "react": "^18.0.0",
                    "react-dom": "^18.0.0",
                    "typescript": "^4.0.0",
                    "next": "^13.0.0",
                    "tailwindcss": "^3.0.0",
                    "@types/react": "^18.0.0",
                    "@types/node": "^18.0.0",
                    "axios": "^1.0.0",
                    "framer-motion": "^10.0.0",
                    "lucide-react": "^0.263.0"
                },
                "devDependencies": {
                    "eslint": "^8.0.0",
                    "prettier": "^2.8.0",
                    "@typescript-eslint/eslint-plugin": "^5.0.0",
                    "autoprefixer": "^10.4.0",
                    "postcss": "^8.4.0"
                }
            },
            "requirements.txt": None
        },
        "backend-housing-hub-saas": {
            "type": "TypeScript Backend",
            "package.json": {
                "dependencies": {
                    "express": "^4.18.0",
                    "typescript": "^4.0.0",
                    "cors": "^2.8.5",
                    "helmet": "^6.0.0",
                    "dotenv": "^16.0.0",
                    "bcrypt": "^5.0.0",
                    "jsonwebtoken": "^8.5.0",
                    "pg": "^8.8.0",
                    "redis": "^4.0.0",
                    "winston": "^3.8.0"
                },
                "devDependencies": {
                    "@types/express": "^4.17.0",
                    "@types/node": "^18.0.0",
                    "@types/cors": "^2.8.0",
                    "@types/bcrypt": "^5.0.0",
                    "@types/jsonwebtoken": "^8.5.0",
                    "@types/pg": "^8.6.0",
                    "ts-node": "^10.9.0",
                    "nodemon": "^2.0.0",
                    "jest": "^29.0.0",
                    "@types/jest": "^29.0.0"
                }
            },
            "requirements.txt": None
        },
        "IAbackend-inmoIA": {
            "type": "Python AI Backend",
            "package.json": None,
            "requirements.txt": [
                "fastapi==0.100.0",
                "uvicorn==0.23.0",
                "pydantic==2.0.0",
                "sqlalchemy==2.0.0",
                "psycopg2-binary==2.9.0",
                "redis==4.6.0",
                "openai==0.28.0",
                "tensorflow==2.13.0",
                "pandas==2.0.0",
                "numpy==1.24.0",
                "scikit-learn==1.3.0",
                "pillow==10.0.0",
                "python-multipart==0.0.6",
                "python-jose==3.3.0",
                "passlib==1.7.4",
                "bcrypt==4.0.1"
            ]
        },
        "FacturaIA": {
            "type": "Full-Stack Application",
            "package.json": {
                "dependencies": {
                    "react": "^18.0.0",
                    "typescript": "^4.0.0",
                    "express": "^4.18.0",
                    "node": "^18.0.0",
                    "mongodb": "^5.0.0",
                    "mongoose": "^7.0.0",
                    "bcrypt": "^5.0.0",
                    "jsonwebtoken": "^8.5.0",
                    "multer": "^1.4.0",
                    "nodemailer": "^6.9.0"
                },
                "devDependencies": {
                    "eslint": "^8.0.0",
                    "jest": "^29.0.0",
                    "@types/react": "^18.0.0",
                    "@types/express": "^4.17.0",
                    "nodemon": "^2.0.0"
                }
            },
            "requirements.txt": None
        },
        "restaurant-app": {
            "type": "Restaurant Management System",
            "package.json": {
                "dependencies": {
                    "react": "^18.0.0",
                    "typescript": "^4.0.0",
                    "express": "^4.18.0",
                    "node": "^18.0.0",
                    "postgresql": "^8.0.0",
                    "sequelize": "^6.0.0",
                    "bcrypt": "^5.0.0",
                    "jsonwebtoken": "^8.5.0",
                    "stripe": "^12.0.0",
                    "socket.io": "^4.7.0"
                },
                "devDependencies": {
                    "eslint": "^8.0.0",
                    "jest": "^29.0.0",
                    "@types/react": "^18.0.0",
                    "@types/express": "^4.17.0",
                    "nodemon": "^2.0.0"
                }
            },
            "requirements.txt": None
        }
    }
    
    for repo_name, mock_data in mock_repos.items():
        print(f"\n🏗️  Analyzing: {repo_name}")
        print(f"   Type: {mock_data['type']}")
        print("-" * 40)
        
        # Create mock repository
        mock_repo_path = Path(f"../test-{repo_name}")
        mock_repo_path.mkdir(exist_ok=True)
        
        # Create package.json if specified
        if mock_data['package.json']:
            with open(mock_repo_path / "package.json", "w") as f:
                json.dump(mock_data['package.json'], f, indent=2)
            print(f"   ✅ Created package.json with {len(mock_data['package.json']['dependencies'])} dependencies")
            print(f"   ✅ Created package.json with {len(mock_data['package.json']['devDependencies'])} devDependencies")
        
        # Create requirements.txt if specified
        if mock_data['requirements.txt']:
            with open(mock_repo_path / "requirements.txt", "w") as f:
                f.write("\n".join(mock_data['requirements.txt']))
            print(f"   ✅ Created requirements.txt with {len(mock_data['requirements.txt'])} packages")
        
        # Analyze dependencies
        tech_stack = analyzer.analyze_repository_dependencies(mock_repo_path)
        
        # Convert to serializable format
        tech_stack_serializable = {}
        for category, techs in tech_stack.items():
            tech_list = sorted(list(techs))
            tech_stack_serializable[category] = {
                'technologies': tech_list,
                'count': len(tech_list)
            }
        
        # Display results
        print(f"\n📊 Extracted Technologies for {repo_name}:")
        for category, data in tech_stack_serializable.items():
            if data['technologies']:
                print(f"   {category.upper()}:")
                for tech in data['technologies']:
                    print(f"     • {tech}")
                print(f"     Total: {data['count']} technologies")
            else:
                print(f"   {category.upper()}: No technologies detected")
        
        # Save debug output
        debug_file = f"debug_{repo_name}_tech_stack.json"
        with open(debug_file, 'w', encoding='utf-8') as f:
            json.dump(tech_stack_serializable, f, indent=2, ensure_ascii=False)
        print(f"   💾 Saved debug output to: {debug_file}")
        
        # Cleanup
        import shutil
        if mock_repo_path.exists():
            shutil.rmtree(mock_repo_path)
        
        print("-" * 40)
    
    print("\n🎯 Summary of Technology Detection:")
    print("=" * 60)
    
    # Show what each repository should detect
    expected_tech = {
        "housing-hub-saas": {
            "frontend": ["React", "TypeScript", "Next.js", "TailwindCSS", "Framer Motion"],
            "backend": [],
            "database": [],
            "devops": [],
            "ai_ml": []
        },
        "backend-housing-hub-saas": {
            "frontend": ["TypeScript"],
            "backend": ["Express.js", "Node.js"],
            "database": ["PostgreSQL", "Redis"],
            "devops": [],
            "ai_ml": []
        },
        "IAbackend-inmoIA": {
            "frontend": [],
            "backend": ["FastAPI", "Python", "Pydantic"],
            "database": ["PostgreSQL", "SQLAlchemy", "psycopg2", "Redis"],
            "devops": [],
            "ai_ml": ["OpenAI", "TensorFlow", "Pandas", "NumPy", "Scikit-learn"]
        },
        "FacturaIA": {
            "frontend": ["React", "TypeScript"],
            "backend": ["Express.js", "Node.js"],
            "database": ["MongoDB"],
            "devops": [],
            "ai_ml": []
        },
        "restaurant-app": {
            "frontend": ["React", "TypeScript"],
            "backend": ["Express.js", "Node.js"],
            "database": ["PostgreSQL", "Sequelize"],
            "devops": [],
            "ai_ml": []
        }
    }
    
    for repo_name, expected in expected_tech.items():
        print(f"\n📋 {repo_name} Expected Technologies:")
        for category, techs in expected.items():
            if techs:
                print(f"   {category}: {', '.join(techs)}")
    
    print("\n✅ Debug analysis complete!")

if __name__ == "__main__":
    debug_repository_technologies() 
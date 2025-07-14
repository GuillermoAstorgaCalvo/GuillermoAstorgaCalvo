#!/usr/bin/env python3
"""
Dependency Analyzer
Analyzes package.json and requirements.txt files to extract actual technologies and frameworks used.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Any
import subprocess


class DependencyAnalyzer:
    """Analyzes dependencies from package.json and requirements.txt files."""
    
    def __init__(self):
        """Initialize the dependency analyzer."""
        
        # Technology mappings
        self.frontend_tech = {
            'react': 'React', 'react-dom': 'React', '@types/react': 'React',
            'vue': 'Vue.js', '@vue/cli': 'Vue.js', 'vue-router': 'Vue.js',
            'angular': 'Angular', '@angular/core': 'Angular', '@angular/common': 'Angular',
            'next': 'Next.js', 'next.js': 'Next.js', '@next/font': 'Next.js',
            'tailwindcss': 'TailwindCSS', 'tailwind': 'TailwindCSS', '@tailwindcss/forms': 'TailwindCSS',
            'bootstrap': 'Bootstrap', '@bootstrap': 'Bootstrap',
            'framer-motion': 'Framer Motion', 'framer': 'Framer Motion',
            'styled-components': 'Styled Components', 'styled': 'Styled Components',
            'sass': 'Sass', 'scss': 'Sass', 'node-sass': 'Sass',
            'less': 'Less',
            'typescript': 'TypeScript', '@types/node': 'TypeScript', '@types/react': 'TypeScript',
            'javascript': 'JavaScript', 'js': 'JavaScript',
            'axios': 'Axios', 'fetch': 'Fetch API',
            'lodash': 'Lodash', 'underscore': 'Underscore',
            'moment': 'Moment.js', 'date-fns': 'date-fns',
            'chart.js': 'Chart.js', 'd3': 'D3.js', 'recharts': 'Recharts'
        }
        
        self.backend_tech = {
            'express': 'Express.js', 'express.js': 'Express.js', '@types/express': 'Express.js',
            'fastapi': 'FastAPI', 'fast-api': 'FastAPI', 'uvicorn': 'FastAPI',
            'django': 'Django', 'djangorestframework': 'Django REST', 'django-cors-headers': 'Django',
            'flask': 'Flask', 'flask-cors': 'Flask',
            'node': 'Node.js', 'nodejs': 'Node.js',
            'python': 'Python',
            'java': 'Java', 'spring-boot': 'Spring Boot', 'spring': 'Spring',
            'php': 'PHP', 'laravel': 'Laravel', 'symfony': 'Symfony',
            'ruby': 'Ruby', 'rails': 'Ruby on Rails',
            'go': 'Go', 'golang': 'Go',
            'rust': 'Rust',
            'cors': 'CORS', 'helmet': 'Helmet',
            'bcrypt': 'bcrypt', 'jsonwebtoken': 'JWT', 'passport': 'Passport'
        }
        
        self.database_tech = {
            'postgresql': 'PostgreSQL', 'pg': 'PostgreSQL', 'postgres': 'PostgreSQL', 'postgresql-client': 'PostgreSQL',
            'mysql': 'MySQL', 'mysql2': 'MySQL', 'mysql-connector': 'MySQL',
            'mongodb': 'MongoDB', 'mongoose': 'MongoDB', 'mongodb-driver': 'MongoDB',
            'redis': 'Redis', 'ioredis': 'Redis',
            'sqlite': 'SQLite', 'sqlite3': 'SQLite',
            'prisma': 'Prisma', '@prisma/client': 'Prisma',
            'sequelize': 'Sequelize', 'sequelize-cli': 'Sequelize',
            'sqlalchemy': 'SQLAlchemy', 'alembic': 'SQLAlchemy',
            'typeorm': 'TypeORM', 'typeorm-reflect-metadata': 'TypeORM'
        }
        
        self.devops_tech = {
            'docker': 'Docker', 'docker-compose': 'Docker Compose', '@types/docker': 'Docker',
            'kubernetes': 'Kubernetes', 'k8s': 'Kubernetes',
            'aws': 'AWS', 'aws-sdk': 'AWS SDK', '@aws-sdk/client-s3': 'AWS',
            'azure': 'Azure', '@azure/identity': 'Azure', '@azure/storage-blob': 'Azure',
            'gcp': 'Google Cloud', 'google-cloud': 'Google Cloud', '@google-cloud/storage': 'Google Cloud',
            'terraform': 'Terraform',
            'jenkins': 'Jenkins',
            'github-actions': 'GitHub Actions',
            'gitlab-ci': 'GitLab CI',
            'nginx': 'Nginx', 'apache': 'Apache'
        }
        
        self.ai_ml_tech = {
            'openai': 'OpenAI', 'openai-api': 'OpenAI', '@openai/api': 'OpenAI',
            'tensorflow': 'TensorFlow', 'tf': 'TensorFlow', 'tensorflow-gpu': 'TensorFlow',
            'pytorch': 'PyTorch', 'torch': 'PyTorch', 'torchvision': 'PyTorch',
            'scikit-learn': 'Scikit-learn', 'sklearn': 'Scikit-learn',
            'pandas': 'Pandas',
            'numpy': 'NumPy',
            'matplotlib': 'Matplotlib',
            'seaborn': 'Seaborn',
            'transformers': 'Transformers', 'huggingface': 'Hugging Face',
            'langchain': 'LangChain', 'langchain-community': 'LangChain',
            'anthropic': 'Anthropic', 'claude': 'Anthropic',
            'spacy': 'spaCy', 'nltk': 'NLTK'
        }
    
    def analyze_repository_dependencies(self, repo_path: Path) -> Dict[str, Set[str]]:
        """Analyze dependencies from a repository."""
        categories = {
            'frontend': set(),
            'backend': set(),
            'database': set(),
            'devops': set(),
            'ai_ml': set()
        }
        
        # Look for package.json files
        package_json_files = list(repo_path.rglob('package.json'))
        for package_file in package_json_files:
            try:
                with open(package_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Analyze dependencies
                deps = data.get('dependencies', {})
                dev_deps = data.get('devDependencies', {})
                all_deps = {**deps, **dev_deps}
                
                for dep_name, version in all_deps.items():
                    dep_lower = dep_name.lower()
                    
                    # Categorize the dependency
                    if dep_lower in self.frontend_tech:
                        categories['frontend'].add(self.frontend_tech[dep_lower])
                    elif dep_lower in self.backend_tech:
                        categories['backend'].add(self.backend_tech[dep_lower])
                    elif dep_lower in self.database_tech:
                        categories['database'].add(self.database_tech[dep_lower])
                    elif dep_lower in self.devops_tech:
                        categories['devops'].add(self.devops_tech[dep_lower])
                    elif dep_lower in self.ai_ml_tech:
                        categories['ai_ml'].add(self.ai_ml_tech[dep_lower])
                        
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"⚠️ Could not parse {package_file}: {e}")
        
        # Look for requirements.txt files
        requirements_files = list(repo_path.rglob('requirements.txt'))
        for req_file in requirements_files:
            try:
                with open(req_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Extract package name (remove version specifiers)
                        package_name = re.split(r'[=<>!~]', line)[0].lower()
                        
                        # Categorize the package
                        if package_name in self.backend_tech:
                            categories['backend'].add(self.backend_tech[package_name])
                        elif package_name in self.database_tech:
                            categories['database'].add(self.database_tech[package_name])
                        elif package_name in self.devops_tech:
                            categories['devops'].add(self.devops_tech[package_name])
                        elif package_name in self.ai_ml_tech:
                            categories['ai_ml'].add(self.ai_ml_tech[package_name])
                            
            except FileNotFoundError as e:
                print(f"⚠️ Could not read {req_file}: {e}")
        
        return categories
    
    def analyze_all_repositories(self, repos_dir: Path) -> Dict[str, Any]:
        """Analyze dependencies from all repositories."""
        all_technologies = {
            'frontend': set(),
            'backend': set(),
            'database': set(),
            'devops': set(),
            'ai_ml': set()
        }
        
        # Look for repositories in the repos directory
        if repos_dir.exists():
            for repo_dir in repos_dir.iterdir():
                if repo_dir.is_dir():
                    print(f"🔍 Analyzing dependencies in {repo_dir.name}")
                    repo_tech = self.analyze_repository_dependencies(repo_dir)
                    
                    # Merge technologies
                    for category, techs in repo_tech.items():
                        all_technologies[category].update(techs)
        
        # Convert sets to sorted lists
        result = {}
        for category, techs in all_technologies.items():
            result[category] = {
                'technologies': sorted(list(techs)),
                'count': len(techs)
            }
        
        return result


def main():
    """Main function to analyze dependencies."""
    analyzer = DependencyAnalyzer()
    
    # Look for repositories in the current directory or a repos subdirectory
    current_dir = Path.cwd()
    repos_dir = current_dir / 'repos'
    
    if not repos_dir.exists():
        # Try to find repositories in the current directory
        repos_dir = current_dir
    
    print(f"🔍 Analyzing dependencies in: {repos_dir}")
    
    tech_stack = analyzer.analyze_all_repositories(repos_dir)
    
    # Print results
    print("\n📊 Technology Stack Analysis:")
    for category, data in tech_stack.items():
        if data['technologies']:
            print(f"\n{category.title()}:")
            for tech in data['technologies']:
                print(f"  • {tech}")
    
    # Save results
    output_file = current_dir / 'tech_stack_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tech_stack, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Technology stack analysis saved to: {output_file}")


if __name__ == "__main__":
    main() 
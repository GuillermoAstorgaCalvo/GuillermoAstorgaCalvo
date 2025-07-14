#!/usr/bin/env python3
"""
Professional Dynamic README Generator
Creates an authentic, human-written GitHub profile README
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

def load_analytics_data() -> Dict[str, Any]:
    """Load analytics data from JSON file in project root"""
    try:
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        analytics_path = os.path.join(root_dir, 'analytics_history.json')
        unified_stats_path = os.path.join(root_dir, 'unified_stats.json')
        
        # Load analytics history
        analytics_data = []
        if os.path.exists(analytics_path):
            with open(analytics_path, 'r', encoding='utf-8') as f:
                analytics_data = json.load(f)
        
        # Load enhanced unified stats
        unified_stats = {}
        if os.path.exists(unified_stats_path):
            with open(unified_stats_path, 'r', encoding='utf-8') as f:
                unified_stats = json.load(f)
        
        return {
            'analytics_history': analytics_data,
            'unified_stats': unified_stats
        }
    except FileNotFoundError:
        print("Warning: analytics_history.json or unified_stats.json not found in project root")
        return {}

def format_number(num: int) -> str:
    """Format large numbers with commas"""
    return f"{num:,}"

def get_project_descriptions() -> Dict[str, Dict[str, Any]]:
    """Get comprehensive project descriptions with authentic narratives"""
    return {
        "InmoIA Frontend": {
            "description": "A real estate platform that actually helps people find their perfect home. Started as a simple listing site and grew into something much bigger.",
            "tech_stack": ["React", "TypeScript", "TailwindCSS", "Next.js"],
            "features": ["AI Property Matching", "Virtual Tours", "Analytics Dashboard"],
            "status": "🟢 Active Development",
            "url": "https://github.com/guillermo-affiliaction/housing-hub-saas",
            "story": "This one started small - just a basic property listing. But as I worked on it, I kept thinking 'what if we could make this smarter?' Now it's a full SaaS platform. The journey from simple to complex taught me so much about scaling React apps."
        },
        "TypeScript Backend": {
            "description": "The engine that powers everything. Built this microservices architecture to handle the heavy lifting - authentication, data processing, you name it.",
            "tech_stack": ["Node.js", "TypeScript", "PostgreSQL", "Docker"],
            "features": ["REST APIs", "Authentication", "Database Management"],
            "status": "🟢 Active Development",
            "url": "https://github.com/guillermo-affiliaction/backend-housing-hub-saas",
            "story": "TypeScript changed everything for me. The first time I refactored this backend with proper types, I realized what I'd been missing. Now I can't imagine building anything complex without it."
        },
        "Python AI MCP Backend": {
            "description": "This is where things get interesting. Built an AI backend that can understand what you're asking and actually do something about it.",
            "tech_stack": ["Python", "FastAPI", "OpenAI", "PostgreSQL"],
            "features": ["AI Task Completion", "Natural Language Processing", "MCP Integration"],
            "status": "🟢 Active Development",
            "url": "https://github.com/guillermo-affiliaction/IAbackend-inmoIA",
            "story": "I was skeptical about AI at first, but seeing this system understand natural language requests blew my mind. It's like having a really smart assistant that actually gets things done."
        },
        "FacturaIA": {
            "description": "Got tired of manually processing invoices, so I built something to do it for me. Sometimes the best projects come from solving your own problems.",
            "tech_stack": ["Python", "React", "TypeScript", "PostgreSQL"],
            "features": ["OCR Processing", "Data Extraction", "Invoice Management"],
            "status": "🟡 In Development",
            "url": "https://github.com/GuillermoAstorgaCalvo/FacturaIA",
            "story": "This was born from pure frustration. I was manually processing invoices one day and thought 'there has to be a better way.' Turns out there was - I just had to build it."
        },
        "Restaurant App": {
            "description": "My first full-stack project that actually went live. Built it for a friend's restaurant and it's still running today.",
            "tech_stack": ["React", "Node.js", "MongoDB", "Express.js"],
            "features": ["Order Management", "Menu System", "Admin Dashboard"],
            "status": "🟢 Live",
            "url": "https://restauranteguillermoastorga.up.railway.app/",
            "story": "This was the project that made me realize I could actually build things people would use. Seeing real customers place orders through something I built was incredibly satisfying."
        }
    }

def generate_hero_section() -> str:
    """Generate authentic hero section with personal touch"""
    return """# 👋 Hey! I'm Guillermo

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=28&pause=1000&color=58A6FF&center=true&vCenter=true&width=600&height=100&lines=Full-Stack+Developer;AI+Enthusiast;Problem+Solver;Code+Craftsman" alt="Typing SVG" />
</div>

I build things. Sometimes they work, sometimes they don't, but I always learn something along the way. Whether it's a simple script or a complex AI system, I love the challenge of turning ideas into reality.

<div align="center">
  <img src="https://img.shields.io/badge/Full--Stack%20Developer-React%20%7C%20Node.js%20%7C%20Python-58A6FF?style=for-the-badge&logo=github&logoColor=white" alt="Full-Stack Developer" />
  <img src="https://img.shields.io/badge/AI%20Enthusiast-Machine%20Learning%20%7C%20NLP-4ECDC4?style=for-the-badge&logo=github&logoColor=white" alt="AI Enthusiast" />
  <img src="https://img.shields.io/badge/Problem%20Solver-Clean%20Code%20%7C%20Best%20Practices-FF6B6B?style=for-the-badge&logo=github&logoColor=white" alt="Problem Solver" />
</div>

---

"""

def generate_about_section() -> str:
    """Generate personal about section"""
    return """## 🚀 What I'm Up To

### 💼 **My Story**
I started coding because I wanted to build things that could actually help people. What began as simple scripts has turned into a passion for creating meaningful applications. I love the challenge of taking a complex problem and turning it into something elegant and useful.

**🔭 Right now:** Working on AI-powered real estate platforms and trying to make invoice processing less painful  
**🌱 Learning:** New AI/ML techniques, microservices, and whatever catches my interest  
**👯 Looking for:** Cool projects to collaborate on, especially open source stuff  
**💬 Ask me about:** React, TypeScript, Python, AI/ML, or anything tech-related - I love talking shop!  
**📫 Get in touch:** [LinkedIn](https://linkedin.com/in/guillermoastorgacalvo) | [Email](mailto:guillermo.astorga.calvo@gmail.com)

### 🎯 **What I Do**
- **Frontend Development**: Building interfaces that people actually want to use
- **Backend Development**: Creating APIs and services that don't break when you need them most
- **AI & ML**: Adding intelligence to applications in ways that actually make sense
- **Database & Cloud**: Making sure data is where it needs to be when it needs to be there
- **DevOps**: Automating the boring stuff so I can focus on building

---

"""

def generate_dynamic_stats_section(data: Dict[str, Any]) -> str:
    """Generate comprehensive stats section using enhanced private repo data"""
    if not data or not isinstance(data, dict):
        return ""
    
    analytics_history = data.get('analytics_history', [])
    unified_stats = data.get('unified_stats', {})
    
    if not analytics_history and not unified_stats:
        return ""
    
    # Use unified stats if available, otherwise fall back to analytics history
    if unified_stats:
        return generate_enhanced_stats_from_unified(unified_stats)
    elif analytics_history:
        return generate_stats_from_analytics(analytics_history)
    
    return ""

def generate_enhanced_stats_from_unified(unified_stats: Dict[str, Any]) -> str:
    """Generate enhanced stats section from comprehensive unified stats"""
    
    # Basic stats badges
    global_summary = unified_stats.get('global_summary', {})
    guillermo_contribution = global_summary.get('guillermo_contribution', {})
    productivity_metrics = unified_stats.get('productivity_metrics', {})
    
    stats_badges = []
    if 'total_loc' in global_summary:
        stats_badges.append(f'<img src="https://img.shields.io/badge/📈_Lines_of_Code-{format_number(global_summary["total_loc"])}-58A6FF?style=for-the-badge&logo=github&logoColor=white" alt="Lines of Code" />')
    
    if 'total_commits' in global_summary:
        stats_badges.append(f'<img src="https://img.shields.io/badge/📝_Commits-{format_number(global_summary["total_commits"])}-4ECDC4?style=for-the-badge&logo=github&logoColor=white" alt="Total Commits" />')
    
    if 'total_files' in global_summary:
        stats_badges.append(f'<img src="https://img.shields.io/badge/📁_Files-{format_number(global_summary["total_files"])}-FF6B6B?style=for-the-badge&logo=github&logoColor=white" alt="Total Files" />')
    
    if 'repositories_processed' in global_summary:
        stats_badges.append(f'<img src="https://img.shields.io/badge/🏢_Repositories-{global_summary["repositories_processed"]}-9C27B0?style=for-the-badge&logo=github&logoColor=white" alt="Repositories" />')
    
    # Personal contribution insights
    contribution_insights = ""
    if guillermo_contribution:
        percentages = guillermo_contribution.get('percentages', {})
        contribution_insights = f"\n### **👨‍💻 My Contributions**\n"
        contribution_insights += f"🎯 **{percentages.get('loc', 0):.1f}% of all code** ({format_number(guillermo_contribution.get('loc', 0))} lines)\n"
        contribution_insights += f"📝 **{format_number(guillermo_contribution.get('commits', 0))} commits** across all projects\n"
        contribution_insights += f"📁 **{format_number(guillermo_contribution.get('files', 0))} files** created or modified\n"
    
    # Productivity metrics
    productivity_insights = ""
    if productivity_metrics:
        productivity_insights = f"\n### **⚡ Productivity Metrics**\n"
        productivity_insights += f"🚀 **{productivity_metrics.get('avg_loc_per_commit', 0):.0f} lines per commit**\n"
        productivity_insights += f"📊 **{productivity_metrics.get('avg_files_per_commit', 0):.1f} files per commit**\n"
        
        code_efficiency = productivity_metrics.get('code_efficiency', {})
        if code_efficiency:
            productivity_insights += f"💡 **{code_efficiency.get('loc_per_file', 0):.0f} lines per file**\n"
    
    # Language breakdown with SVG chart
    language_stats = ""
    language_analysis = unified_stats.get('language_analysis', {})
    if language_analysis:
        # Sort languages by lines of code
        sorted_languages = sorted(language_analysis.items(), key=lambda x: x[1]['lines'], reverse=True)[:5]
        language_stats = "\n### **💻 Top Languages**\n\n"
        language_stats += '<p align="center">\n'
        language_stats += '  <img src="assets/language_stats.svg" alt="Languages by Lines of Code" width="500" />\n'
        language_stats += '</p>\n'
    
    # Tech stack analysis with skillicons.dev
    tech_stack_insights = ""
    tech_stack_analysis = unified_stats.get('tech_stack_analysis', {})
    print(f"🛠️ Rendering tech stack section: {tech_stack_analysis}")
    if tech_stack_analysis:
        # Map actual technologies to skillicons.dev icons
        tech_to_icon = {
            # Frontend
            'React': 'react', 'TypeScript': 'ts', 'JavaScript': 'js', 'Next.js': 'nextjs',
            'TailwindCSS': 'tailwind', 'HTML': 'html', 'CSS': 'css', 'Vue.js': 'vuejs',
            'Angular': 'angular', 'Framer Motion': 'framer', 'Radix UI': 'radix',
            'TanStack Query': 'tanstack', 'React Router': 'reactrouter',
            
            # Backend
            'Node.js': 'nodejs', 'Python': 'python', 'Express.js': 'express',
            'FastAPI': 'fastapi', 'Django': 'django', 'Flask': 'flask',
            'TypeScript': 'ts', 'Java': 'java', 'Spring Boot': 'spring',
            
            # Database & Cloud
            'PostgreSQL': 'postgresql', 'MongoDB': 'mongodb', 'Redis': 'redis',
            'AWS': 'aws', 'Docker': 'docker', 'Supabase': 'supabase',
            'MySQL': 'mysql', 'SQLite': 'sqlite', 'Prisma': 'prisma',
            
            # AI & ML
            'TensorFlow': 'tensorflow', 'PyTorch': 'pytorch', 'Scikit-learn': 'scikit',
            'OpenAI': 'openai', 'Pandas': 'pandas', 'NumPy': 'numpy',
            'Tesseract OCR': 'tesseract', 'Pillow': 'pillow',
            
            # DevOps & Tools
            'Git': 'git', 'GitHub': 'github', 'VS Code': 'vscode',
            'Linux': 'linux', 'Docker Compose': 'docker', 'Nginx': 'nginx',
            'ESLint': 'eslint', 'TypeScript': 'ts', 'Webpack': 'webpack',
            
            # Additional
            'Stripe': 'stripe', 'Framer Motion': 'framer', 'Radix UI': 'radix',
            'TanStack Query': 'tanstack', 'Zod': 'zod', 'Lodash': 'lodash',
            'Axios': 'axios', 'Moment.js': 'moment', 'Chart.js': 'chartjs'
        }
        
        # Build dynamic tech stack
        dynamic_tech_stack = {
            'frontend': [],
            'backend': [],
            'database': [],
            'ai_ml': [],
            'devops': [],
            'additional': []
        }
        
        # Process each category
        for category, data in tech_stack_analysis.items():
            technologies = data.get('technologies', [])
            for tech in technologies:
                icon = tech_to_icon.get(tech, tech.lower().replace(' ', '').replace('.', ''))
                if category == 'frontend':
                    dynamic_tech_stack['frontend'].append(icon)
                elif category == 'backend':
                    dynamic_tech_stack['backend'].append(icon)
                elif category == 'database':
                    dynamic_tech_stack['database'].append(icon)
                elif category == 'ai_ml':
                    dynamic_tech_stack['ai_ml'].append(icon)
                elif category == 'devops':
                    dynamic_tech_stack['devops'].append(icon)
                else:
                    dynamic_tech_stack['additional'].append(icon)
        
        # Generate tech stack section
        tech_stack_insights = "\n### **🛠️ Technology Stack**\n\n"
        tech_stack_insights += "I believe in using the right tool for the job. Here's my current technology stack based on my projects:\n\n"
        
        # Frontend
        if dynamic_tech_stack['frontend']:
            icons = ','.join(dynamic_tech_stack['frontend'][:8])
            tech_stack_insights += f"""#### **🌐 Frontend Development**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Frontend Technologies" />
</div>

"""
        
        # Backend
        if dynamic_tech_stack['backend']:
            icons = ','.join(dynamic_tech_stack['backend'][:8])
            tech_stack_insights += f"""#### **⚙️ Backend Development**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Backend Technologies" />
</div>

"""
        
        # Database & Cloud
        if dynamic_tech_stack['database']:
            icons = ','.join(dynamic_tech_stack['database'][:8])
            tech_stack_insights += f"""#### **🗄️ Database & Cloud**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Database & Cloud Technologies" />
</div>

"""
        
        # AI & ML
        if dynamic_tech_stack['ai_ml']:
            icons = ','.join(dynamic_tech_stack['ai_ml'][:8])
            tech_stack_insights += f"""#### **🤖 AI & Machine Learning**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="AI & ML Technologies" />
</div>

"""
        
        # DevOps & Tools
        if dynamic_tech_stack['devops']:
            icons = ','.join(dynamic_tech_stack['devops'][:8])
            tech_stack_insights += f"""#### **🛠️ Development Tools**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Development Tools" />
</div>

"""
        
        # Additional Technologies
        if dynamic_tech_stack['additional']:
            icons = ','.join(dynamic_tech_stack['additional'][:8])
            tech_stack_insights += f"""#### **📊 Additional Technologies**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Additional Technologies" />
</div>

"""
    
    # Repository insights
    repo_insights = ""
    repo_analysis = unified_stats.get('repository_analysis', {})
    if repo_analysis:
        # Sort repositories by Guillermo's contribution
        sorted_repos = sorted(repo_analysis.items(), 
                            key=lambda x: x[1]['guillermo_stats'].get('loc', 0), reverse=True)[:3]
        
        repo_insights = f"\n### **🏢 Top Projects**\n"
        for repo_name, repo_data in sorted_repos:
            guillermo_stats = repo_data.get('guillermo_stats', {})
            percentages = repo_data.get('percentages', {})
            repo_insights += f"• **{repo_name}** - {format_number(guillermo_stats.get('loc', 0))} lines ({percentages.get('loc', 0):.1f}% contribution)\n"
    
    # Insights
    insights_section = ""
    insights = unified_stats.get('insights', {})
    if insights:
        insights_section = f"\n### **💡 Key Insights**\n"
        
        achievements = insights.get('achievements', [])
        if achievements:
            insights_section += f"🏆 **Achievements:**\n"
            for achievement in achievements[:2]:  # Show top 2 achievements
                insights_section += f"• {achievement}\n"
        
        strengths = insights.get('strengths', [])
        if strengths:
            insights_section += f"\n💪 **Strengths:**\n"
            for strength in strengths[:2]:  # Show top 2 strengths
                insights_section += f"• {strength}\n"

    # Other/Unknown breakdown
    other_unknown_section = ""
    other_unknown = unified_stats.get('other_unknown_breakdown', {})
    if other_unknown and (other_unknown.get('other', 0) > 0 or other_unknown.get('unknown', 0) > 0):
        other_unknown_section = "\n### **🗂️ Other/Unknown Files**\n"
        if other_unknown.get('other', 0) > 0:
            other_unknown_section += f"• **Other:** {format_number(other_unknown['other'])} lines\n"
        if other_unknown.get('unknown', 0) > 0:
            other_unknown_section += f"• **Unknown:** {format_number(other_unknown['unknown'])} lines\n"

    # Validation warning
    validation_section = ""
    validation = unified_stats.get('validation_results', {})
    if validation:
        if validation.get('loc_mismatch') or validation.get('files_mismatch') or validation.get('commits_mismatch'):
            validation_section = ("\n> ⚠️ **Note:** There is a mismatch between the sum of language/project stats and the global totals. "
                                 "This may be due to unclassified files, multi-language files, or aggregation logic.\n")

    return f"""## 📊 **My Private Repository Stats**

> 📊 **Real data from my private enterprise repositories**  
> _Updated every Monday - this is where the real work happens!_

<!-- Dynamic Stats Overview -->
<div align="center">
  {'  '.join(stats_badges)}
</div>

{contribution_insights}

{productivity_insights}

{language_stats}

{tech_stack_insights}

{repo_insights}

{insights_section}

{other_unknown_section}

{validation_section}

These numbers tell the real story - late nights debugging, moments of breakthrough, and a lot of trial and error. Every line of code represents a problem solved or something new learned. The private repos are where the magic happens!

---

"""

def generate_stats_from_analytics(analytics_history: List[Dict[str, Any]]) -> str:
    """Generate stats section from analytics history (fallback)"""
    if not analytics_history or len(analytics_history) == 0:
        return ""
    
    latest_data = analytics_history[-1]  # Get the most recent data
    
    # Basic stats badges
    stats_badges = []
    if 'total_loc' in latest_data:
        stats_badges.append(f'<img src="https://img.shields.io/badge/📈_Lines_of_Code-{format_number(latest_data["total_loc"])}-58A6FF?style=for-the-badge&logo=github&logoColor=white" alt="Lines of Code" />')
    
    if 'total_commits' in latest_data:
        stats_badges.append(f'<img src="https://img.shields.io/badge/📝_Commits-{format_number(latest_data["total_commits"])}-4ECDC4?style=for-the-badge&logo=github&logoColor=white" alt="Total Commits" />')
    
    if 'total_files' in latest_data:
        stats_badges.append(f'<img src="https://img.shields.io/badge/📁_Files-{format_number(latest_data["total_files"])}-FF6B6B?style=for-the-badge&logo=github&logoColor=white" alt="Total Files" />')
    
    if 'repos_processed' in latest_data:
        stats_badges.append(f'<img src="https://img.shields.io/badge/🏢_Repositories-{latest_data["repos_processed"]}-9C27B0?style=for-the-badge&logo=github&logoColor=white" alt="Repositories" />')
    
    # Personal contribution percentage
    contribution_insights = ""
    if 'guillermo_loc' in latest_data and 'total_loc' in latest_data:
        contribution_pct = (latest_data['guillermo_loc'] / latest_data['total_loc']) * 100 if latest_data['total_loc'] > 0 else 0
        contribution_insights = f"\n### **👨‍💻 My Contributions**\n"
        contribution_insights += f"🎯 **{contribution_pct:.1f}% of all code** ({format_number(latest_data['guillermo_loc'])} lines)\n"
        if 'guillermo_commits' in latest_data:
            contribution_insights += f"📝 **{format_number(latest_data['guillermo_commits'])} commits** across all projects\n"
        if 'guillermo_files' in latest_data:
            contribution_insights += f"📁 **{format_number(latest_data['guillermo_files'])} files** created or modified\n"
    
    return f"""## 📊 **My Private Repository Stats**

> 📊 **Real data from my private enterprise repositories**  
> _Updated every Monday - this is where the real work happens!_

<!-- Dynamic Stats Overview -->
<div align="center">
  {'  '.join(stats_badges)}
</div>

{contribution_insights}

These numbers tell the real story - late nights debugging, moments of breakthrough, and a lot of trial and error. Every line of code represents a problem solved or something new learned. The private repos are where the magic happens!

---

"""

def generate_projects_section() -> str:
    """Generate authentic projects section with personal stories"""
    projects = get_project_descriptions()
    
    content = """## 🚀 **Stuff I've Built**

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=20&pause=1000&color=58A6FF&center=true&vCenter=true&width=500&height=50&lines=Innovative+SaaS+Solutions;AI-Powered+Applications;Modern+Web+Platforms" alt="Projects Typing" />
</div>

Here are some projects I'm pretty proud of. Each one taught me something different and pushed me to grow.

"""
    
    for project_name, project_info in projects.items():
        tech_stack_badges = []
        for tech in project_info['tech_stack']:
            color_map = {
                'React': '61DAFB',
                'TypeScript': '3178C6',
                'Python': '3776AB',
                'Node.js': '339933',
                'Next.js': '000000',
                'TailwindCSS': '38B2AC',
                'PostgreSQL': '336791',
                'MongoDB': '47A248',
                'Docker': '2496ED',
                'FastAPI': '009688',
                'Express.js': '000000'
            }
            color = color_map.get(tech, '58A6FF')
            tech_stack_badges.append(f'![{tech}](https://img.shields.io/badge/-{tech}-{color}?style=for-the-badge&logo={tech.lower()}&logoColor=white)')
        
        features_list = '\n'.join([f"- {feature}" for feature in project_info['features']])
        
        content += f"""### 🏆 **{project_name}**
{project_info['status']} • {project_info['description']}

**Tech Stack:** {' '.join(tech_stack_badges)}

**What it does:**
{features_list}

**The backstory:** {project_info['story']}

**🔗 [Check it out]({project_info['url']})**

---
"""
    
    return content

def generate_dynamic_tech_stack_section(data: Dict[str, Any]) -> str:
    """Generate dynamic tech stack section using skillicons.dev based on actual repository data"""
    
    # Default tech stack if no data is available
    default_tech_stack = {
        'frontend': ['react', 'ts', 'js', 'nextjs', 'tailwind', 'html', 'css'],
        'backend': ['nodejs', 'python', 'express', 'fastapi'],
        'database': ['postgresql', 'mongodb', 'aws', 'docker'],
        'ai_ml': ['tensorflow', 'scikit', 'openai'],
        'devops': ['git', 'github', 'vscode', 'linux'],
        'additional': ['supabase', 'stripe', 'framer']
    }
    
    # Try to get actual tech stack from unified stats
    unified_stats = data.get('unified_stats', {})
    tech_stack_analysis = unified_stats.get('tech_stack_analysis', {})
    
    if tech_stack_analysis:
        # Map actual technologies to skillicons.dev icons
        tech_to_icon = {
            # Frontend
            'React': 'react', 'TypeScript': 'ts', 'JavaScript': 'js', 'Next.js': 'nextjs',
            'TailwindCSS': 'tailwind', 'HTML': 'html', 'CSS': 'css', 'Vue.js': 'vuejs',
            'Angular': 'angular', 'Framer Motion': 'framer', 'Radix UI': 'radix',
            'TanStack Query': 'tanstack', 'React Router': 'reactrouter',
            
            # Backend
            'Node.js': 'nodejs', 'Python': 'python', 'Express.js': 'express',
            'FastAPI': 'fastapi', 'Django': 'django', 'Flask': 'flask',
            'TypeScript': 'ts', 'Java': 'java', 'Spring Boot': 'spring',
            
            # Database & Cloud
            'PostgreSQL': 'postgresql', 'MongoDB': 'mongodb', 'Redis': 'redis',
            'AWS': 'aws', 'Docker': 'docker', 'Supabase': 'supabase',
            'MySQL': 'mysql', 'SQLite': 'sqlite', 'Prisma': 'prisma',
            
            # AI & ML
            'TensorFlow': 'tensorflow', 'PyTorch': 'pytorch', 'Scikit-learn': 'scikit',
            'OpenAI': 'openai', 'Pandas': 'pandas', 'NumPy': 'numpy',
            'Tesseract OCR': 'tesseract', 'Pillow': 'pillow',
            
            # DevOps & Tools
            'Git': 'git', 'GitHub': 'github', 'VS Code': 'vscode',
            'Linux': 'linux', 'Docker Compose': 'docker', 'Nginx': 'nginx',
            'ESLint': 'eslint', 'TypeScript': 'ts', 'Webpack': 'webpack',
            
            # Additional
            'Stripe': 'stripe', 'Framer Motion': 'framer', 'Radix UI': 'radix',
            'TanStack Query': 'tanstack', 'Zod': 'zod', 'Lodash': 'lodash',
            'Axios': 'axios', 'Moment.js': 'moment', 'Chart.js': 'chartjs'
        }
        
        # Build dynamic tech stack
        dynamic_tech_stack = {
            'frontend': [],
            'backend': [],
            'database': [],
            'ai_ml': [],
            'devops': [],
            'additional': []
        }
        
        # Process each category
        for category, data in tech_stack_analysis.items():
            technologies = data.get('technologies', [])
            for tech in technologies:
                icon = tech_to_icon.get(tech, tech.lower().replace(' ', '').replace('.', ''))
                if category == 'frontend':
                    dynamic_tech_stack['frontend'].append(icon)
                elif category == 'backend':
                    dynamic_tech_stack['backend'].append(icon)
                elif category == 'database':
                    dynamic_tech_stack['database'].append(icon)
                elif category == 'ai_ml':
                    dynamic_tech_stack['ai_ml'].append(icon)
                elif category == 'devops':
                    dynamic_tech_stack['devops'].append(icon)
                else:
                    dynamic_tech_stack['additional'].append(icon)
        
        # Use dynamic tech stack if we have data, otherwise use default
        tech_stack = dynamic_tech_stack if any(any(techs) for techs in dynamic_tech_stack.values()) else default_tech_stack
    else:
        tech_stack = default_tech_stack
    
    # Generate the tech stack section
    content = """## 🛠️ **Technology Stack**

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=18&pause=1000&color=58A6FF&center=true&vCenter=true&width=400&height=40&lines=Modern+Technologies;Best+Practices;Clean+Code" alt="Tech Stack Typing" />
</div>

I believe in using the right tool for the job. Here's my current technology stack based on my projects:

"""
    
    # Frontend
    if tech_stack['frontend']:
        icons = ','.join(tech_stack['frontend'][:8])  # Limit to 8 icons
        content += f"""### **🌐 Frontend Development**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Frontend Technologies" />
</div>

"""
    
    # Backend
    if tech_stack['backend']:
        icons = ','.join(tech_stack['backend'][:8])
        content += f"""### **⚙️ Backend Development**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Backend Technologies" />
</div>

"""
    
    # Database & Cloud
    if tech_stack['database']:
        icons = ','.join(tech_stack['database'][:8])
        content += f"""### **🗄️ Database & Cloud**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Database & Cloud Technologies" />
</div>

"""
    
    # AI & ML
    if tech_stack['ai_ml']:
        icons = ','.join(tech_stack['ai_ml'][:8])
        content += f"""### **🤖 AI & Machine Learning**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="AI & ML Technologies" />
</div>

"""
    
    # DevOps & Tools
    if tech_stack['devops']:
        icons = ','.join(tech_stack['devops'][:8])
        content += f"""### **🛠️ Development Tools**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Development Tools" />
</div>

"""
    
    # Additional Technologies
    if tech_stack['additional']:
        icons = ','.join(tech_stack['additional'][:8])
        content += f"""### **📊 Additional Technologies**
<div align="center">
  <img src="https://skillicons.dev/icons?i={icons}" alt="Additional Technologies" />
</div>

"""
    
    content += "---\n"
    return content

def generate_experience_section() -> str:
    """Generate authentic experience section"""
    return """## 💼 **Experience & Growth**

### **🎯 What I Focus On**
I build full-stack applications that solve real problems. My approach is pretty simple - use modern tools, write clean code, and focus on what actually matters to users. I love working with AI and finding ways to make applications smarter without overcomplicating things.

### **🏆 What I've Done**
- **Built SaaS platforms** that handle real traffic and don't crash
- **Added AI features** that actually improve user experience
- **Maintained code quality** across multiple projects
- **Learned to balance** quick development with long-term maintainability

### **📈 My Journey**
- **Started with simple scripts** and gradually tackled bigger challenges
- **Discovered TypeScript** and realized what I'd been missing
- **Explored AI/ML** and found ways to make it practical
- **Embraced DevOps** to make development less painful

The numbers in my stats aren't just metrics - they're late nights, debugging sessions, and moments of "aha!" Every commit represents a problem solved or something new learned.

---

"""

def generate_contact_section() -> str:
    """Generate authentic contact section"""
    return """## 🌟 **Let's Connect**

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=18&pause=1000&color=58A6FF&center=true&vCenter=true&width=400&height=40&lines=Let%27s+Build+Something+Amazing;Together!" alt="Contact Typing" />
</div>

I'm always up for connecting with fellow developers, discussing interesting projects, or exploring new opportunities. Whether you want to collaborate on something cool, ask about my projects, or just say hello - I'd love to hear from you!

<div align="center">
  <a href="https://linkedin.com/in/guillermoastorgacalvo">
    <img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  <a href="https://github.com/guillermo-affiliaction">
    <img src="https://img.shields.io/badge/-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
  <a href="mailto:guillermo.astorga.calvo@gmail.com">
    <img src="https://img.shields.io/badge/-Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>
  <a href="https://guillermoastorgacalvo.dev">
    <img src="https://img.shields.io/badge/-Portfolio-FF6B6B?style=for-the-badge&logo=github&logoColor=white" alt="Portfolio" />
  </a>
</div>

---

*Last updated: {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}*
"""

def generate_enhanced_readme(data: Dict[str, Any]) -> str:
    """Generate complete enhanced README content"""
    
    content = ""
    
    # Hero Section
    content += generate_hero_section()
    
    # About Section
    content += generate_about_section()
    
    # Dynamic Stats Section
    content += generate_dynamic_stats_section(data)
    
    # Projects Section
    content += generate_projects_section()
    
    # Experience Section
    content += generate_experience_section()
    
    # Contact Section
    content += generate_contact_section()
    
    return content

def main():
    """Main function to generate enhanced README"""
    print("🔄 Generating professional dynamic README...")
    
    # Load analytics data
    data = load_analytics_data()
    
    # Generate enhanced README content
    content = generate_enhanced_readme(data)
    
    # Always write to project root
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    readme_path = os.path.join(root_dir, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Professional README.md generated successfully!")
    print(f"📊 Data source: analytics_history.json")
    print(f"📅 Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"🎨 Features: Authentic content, personal narrative, dynamic stats")

if __name__ == "__main__":
    main() 
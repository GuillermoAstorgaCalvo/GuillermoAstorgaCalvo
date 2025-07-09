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
        with open(analytics_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: analytics_history.json not found in project root")
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
    """Generate comprehensive stats section using private repo data"""
    if not data or not isinstance(data, list) or len(data) == 0:
        return ""
    
    latest_data = data[-1]  # Get the most recent data
    
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
    
    # Language breakdown
    language_stats = ""
    if 'language_stats' in latest_data and latest_data['language_stats']:
        top_languages = sorted(latest_data['language_stats'].items(), key=lambda x: x[1], reverse=True)[:5]
        language_stats = "\n### **💻 Top Languages**\n"
        for lang, lines in top_languages:
            percentage = (lines / latest_data['total_loc']) * 100 if latest_data['total_loc'] > 0 else 0
            language_stats += f"![{lang}](https://img.shields.io/badge/-{lang}-58A6FF?style=for-the-badge&logo={lang.lower()}&logoColor=white) **{percentage:.1f}%** ({format_number(lines)} lines)\n"
    
    # Growth analysis
    growth_insights = ""
    if len(data) > 1:
        previous_data = data[-2]
        if 'total_loc' in latest_data and 'total_loc' in previous_data:
            loc_growth = latest_data['total_loc'] - previous_data['total_loc']
            growth_insights = f"\n### **📈 Growth This Week**\n"
            if loc_growth > 0:
                growth_insights += f"➕ **+{format_number(loc_growth)} lines of code**\n"
            elif loc_growth < 0:
                growth_insights += f"➖ **{format_number(loc_growth)} lines of code** (refactoring)\n"
            else:
                growth_insights += f"➖ **No new code** (maintenance week)\n"
    
    # Repository insights
    repo_insights = ""
    if 'repo_details' in latest_data and latest_data['repo_details']:
        active_repos = len([repo for repo in latest_data['repo_details'] if repo.get('active', True)])
        total_repos = len(latest_data['repo_details'])
        repo_insights = f"\n### **🏢 Repository Overview**\n"
        repo_insights += f"🟢 **{active_repos} active repositories**\n"
        repo_insights += f"📊 **{total_repos} total repositories**\n"
        
        # Show top repos by activity
        top_repos = sorted(latest_data['repo_details'], key=lambda x: x.get('loc', 0), reverse=True)[:3]
        if top_repos:
            repo_insights += f"\n**Most Active Projects:**\n"
            for repo in top_repos:
                repo_insights += f"• **{repo.get('name', 'Unknown')}** - {format_number(repo.get('loc', 0))} lines\n"
    
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

{language_stats}

{growth_insights}

{repo_insights}

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

def generate_tech_stack_section() -> str:
    """Generate authentic tech stack section"""
    return """## 🛠️ **Tools I Use**

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=18&pause=1000&color=58A6FF&center=true&vCenter=true&width=400&height=40&lines=Modern+Technologies;Best+Practices;Clean+Code" alt="Tech Stack Typing" />
</div>

I believe in using the right tool for the job. Here's what I've been working with lately:

### **🌐 Frontend**
![React](https://img.shields.io/badge/-React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/-TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Next.js](https://img.shields.io/badge/-Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/-TailwindCSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Framer Motion](https://img.shields.io/badge/-Framer%20Motion-0055FF?style=for-the-badge&logo=framer&logoColor=white)

### **⚙️ Backend**
![Node.js](https://img.shields.io/badge/-Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Express.js](https://img.shields.io/badge/-Express.js-000000?style=for-the-badge&logo=express&logoColor=white)

### **🗄️ Data & Cloud**
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![MongoDB](https://img.shields.io/badge/-MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![AWS](https://img.shields.io/badge/-AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

### **🤖 AI & ML**
![OpenAI](https://img.shields.io/badge/-OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![TensorFlow](https://img.shields.io/badge/-TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/-Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

### **🛠️ Tools**
![Git](https://img.shields.io/badge/-Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/-GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Linux](https://img.shields.io/badge/-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![VS Code](https://img.shields.io/badge/-VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)

---

"""

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
    
    # Tech Stack Section
    content += generate_tech_stack_section()
    
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
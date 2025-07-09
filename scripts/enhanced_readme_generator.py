#!/usr/bin/env python3
"""
Enhanced Dynamic README Generator
Creates a modern, comprehensive GitHub profile README
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
    """Get comprehensive project descriptions"""
    return {
        "InmoIA Frontend": {
            "description": "Modern real estate SaaS platform with AI-powered property management",
            "tech_stack": ["React", "TypeScript", "TailwindCSS", "Next.js"],
            "features": ["AI Property Matching", "Virtual Tours", "Analytics Dashboard"],
            "status": "🟢 Active Development",
            "url": "https://github.com/guillermo-affiliaction/housing-hub-saas"
        },
        "TypeScript Backend": {
            "description": "Microservices architecture backend for real estate platform",
            "tech_stack": ["Node.js", "TypeScript", "PostgreSQL", "Docker"],
            "features": ["REST APIs", "Authentication", "Database Management"],
            "status": "🟢 Active Development",
            "url": "https://github.com/guillermo-affiliaction/backend-housing-hub-saas"
        },
        "Python AI MCP Backend": {
            "description": "AI-powered backend with task completion and natural language processing",
            "tech_stack": ["Python", "FastAPI", "OpenAI", "PostgreSQL"],
            "features": ["AI Task Completion", "Natural Language Processing", "MCP Integration"],
            "status": "🟢 Active Development",
            "url": "https://github.com/guillermo-affiliaction/IAbackend-inmoIA"
        },
        "FacturaIA": {
            "description": "AI-driven invoice processing system with automated data extraction",
            "tech_stack": ["Python", "React", "TypeScript", "PostgreSQL"],
            "features": ["OCR Processing", "Data Extraction", "Invoice Management"],
            "status": "🟡 In Development",
            "url": "https://github.com/GuillermoAstorgaCalvo/FacturaIA"
        },
        "Restaurant App": {
            "description": "Full-stack restaurant management solution with ordering and analytics",
            "tech_stack": ["React", "Node.js", "MongoDB", "Express.js"],
            "features": ["Order Management", "Menu System", "Admin Dashboard"],
            "status": "🟢 Live",
            "url": "https://restauranteguillermoastorga.up.railway.app/"
        }
    }

def generate_hero_section() -> str:
    """Generate modern hero section with animated elements"""
    return """# 👋 Hi, I'm Guillermo Astorga Calvo

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=28&pause=1000&color=58A6FF&center=true&vCenter=true&width=600&height=100&lines=Full-Stack+Developer;AI+Enthusiast;Problem+Solver;Code+Craftsman" alt="Typing SVG" />
</div>

<div align="center">
  <img src="https://img.shields.io/badge/Full--Stack%20Developer-React%20%7C%20Node.js%20%7C%20Python-58A6FF?style=for-the-badge&logo=github&logoColor=white" alt="Full-Stack Developer" />
  <img src="https://img.shields.io/badge/AI%20Enthusiast-Machine%20Learning%20%7C%20NLP-4ECDC4?style=for-the-badge&logo=github&logoColor=white" alt="AI Enthusiast" />
  <img src="https://img.shields.io/badge/Problem%20Solver-Clean%20Code%20%7C%20Best%20Practices-FF6B6B?style=for-the-badge&logo=github&logoColor=white" alt="Problem Solver" />
</div>

---

"""

def generate_about_section() -> str:
    """Generate about section with personal information"""
    return """## 🚀 About Me

<div align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=GuillermoAstorgaCalvo&show_icons=true&theme=radical&hide_border=true&bg_color=0D1117&title_color=58A6FF&text_color=8B949E&icon_color=58A6FF&include_all_commits=true&count_private=true" alt="GitHub Stats" />
</div>

### 💼 **Professional Summary**
- 🔭 **Currently working on** AI-powered real estate platform and invoice processing systems
- 🌱 **Learning** Advanced AI/ML techniques and microservices architecture
- 👯 **Looking to collaborate on** Open source projects and innovative SaaS solutions
- 💬 **Ask me about** React, TypeScript, Python, AI/ML, and full-stack development
- 📫 **How to reach me** [LinkedIn](https://linkedin.com/in/guillermoastorgacalvo) | [Email](mailto:guillermo.astorga.calvo@gmail.com)

### 🎯 **Core Competencies**
- **Frontend Development**: React, TypeScript, Next.js, TailwindCSS
- **Backend Development**: Node.js, Python, FastAPI, Express.js
- **Database & Cloud**: PostgreSQL, MongoDB, AWS, Docker
- **AI & ML**: OpenAI, Natural Language Processing, Data Analysis
- **DevOps**: CI/CD, GitHub Actions, Linux, Git

---

"""

def generate_dynamic_stats_section(data: Dict[str, Any]) -> str:
    """Generate dynamic statistics section"""
    if not data or not isinstance(data, list) or len(data) == 0:
        return ""
    
    latest_data = data[-1]  # Get the most recent data
    
    stats_badges = []
    if 'total_loc' in latest_data:
        stats_badges.append(f'<img src="https://img.shields.io/badge/📈_Total_Lines_of_Code-{format_number(latest_data["total_loc"])}-58A6FF?style=for-the-badge&logo=github&logoColor=white" alt="Total Lines of Code" />')
    
    if 'total_commits' in latest_data:
        stats_badges.append(f'<img src="https://img.shields.io/badge/📝_Total_Commits-{format_number(latest_data["total_commits"])}-4ECDC4?style=for-the-badge&logo=github&logoColor=white" alt="Total Commits" />')
    
    if 'total_files' in latest_data:
        stats_badges.append(f'<img src="https://img.shields.io/badge/📁_Total_Files-{format_number(latest_data["total_files"])}-FF6B6B?style=for-the-badge&logo=github&logoColor=white" alt="Total Files" />')
    
    if 'repos_processed' in latest_data:
        stats_badges.append(f'<img src="https://img.shields.io/badge/🏢_Repositories-{latest_data["repos_processed"]}-9C27B0?style=for-the-badge&logo=github&logoColor=white" alt="Repositories" />')
    
    return f"""## 📊 **My Coding Journey**

> 📊 **Unified stats from my private enterprise repositories**  
> _Updated automatically every Monday via GitHub Actions_

<!-- Dynamic Stats Overview -->
<div align="center">
  {'  '.join(stats_badges)}
</div>

<!-- GitHub Streak -->
<div align="center">
  <img src="https://streak-stats.demolab.com/?user=GuillermoAstorgaCalvo&theme=radical&hide_border=true&background=0D1117&stroke=58A6FF&ring=58A6FF&fire=58A6FF&currStreakNum=8B949E&sideNums=8B949E&currStreakLabel=8B949E&sideLabels=8B949E&dates=8B949E" alt="GitHub Streak" />
</div>

---

"""

def generate_projects_section() -> str:
    """Generate comprehensive projects section"""
    projects = get_project_descriptions()
    
    content = """## 🚀 **Featured Projects**

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=20&pause=1000&color=58A6FF&center=true&vCenter=true&width=500&height=50&lines=Innovative+SaaS+Solutions;AI-Powered+Applications;Modern+Web+Platforms" alt="Projects Typing" />
</div>

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

**Key Features:**
{features_list}

**🔗 [View Project]({project_info['url']})**

---
"""
    
    return content

def generate_tech_stack_section() -> str:
    """Generate comprehensive tech stack section"""
    return """## 🛠️ **Tech Stack & Skills**

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=18&pause=1000&color=58A6FF&center=true&vCenter=true&width=400&height=40&lines=Modern+Technologies;Best+Practices;Clean+Code" alt="Tech Stack Typing" />
</div>

### **🌐 Frontend Development**
![React](https://img.shields.io/badge/-React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/-TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Next.js](https://img.shields.io/badge/-Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/-TailwindCSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Framer Motion](https://img.shields.io/badge/-Framer%20Motion-0055FF?style=for-the-badge&logo=framer&logoColor=white)

### **⚙️ Backend Development**
![Node.js](https://img.shields.io/badge/-Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Express.js](https://img.shields.io/badge/-Express.js-000000?style=for-the-badge&logo=express&logoColor=white)

### **🗄️ Database & Cloud**
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![MongoDB](https://img.shields.io/badge/-MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![AWS](https://img.shields.io/badge/-AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

### **🤖 AI & Machine Learning**
![OpenAI](https://img.shields.io/badge/-OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![TensorFlow](https://img.shields.io/badge/-TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/-Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

### **🛠️ Tools & DevOps**
![Git](https://img.shields.io/badge/-Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/-GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Linux](https://img.shields.io/badge/-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![VS Code](https://img.shields.io/badge/-VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)

---

"""

def generate_experience_section() -> str:
    """Generate experience and achievements section"""
    return """## 💼 **Experience & Achievements**

### **🎯 Professional Focus**
- **Full-Stack Development**: Building scalable web applications with modern technologies
- **AI Integration**: Implementing AI/ML solutions in production environments
- **SaaS Development**: Creating enterprise-level software-as-a-service platforms
- **Code Quality**: Maintaining high standards with clean code and best practices

### **🏆 Key Achievements**
- **145,000+ Lines of Code**: Across multiple enterprise projects
- **5+ Active Repositories**: Managing complex codebases
- **AI-Powered Solutions**: Successfully implementing AI in production
- **Modern Architecture**: Microservices and scalable system design

### **📈 Growth Metrics**
- **TypeScript Expertise**: 66% of codebase in TypeScript
- **Multi-Language Proficiency**: 9+ programming languages
- **Continuous Learning**: Regular updates and skill development
- **Open Source Contribution**: Active participation in community projects

---

"""

def generate_contact_section() -> str:
    """Generate contact and social links section"""
    return """## 🌟 **Let's Connect**

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=18&pause=1000&color=58A6FF&center=true&vCenter=true&width=400&height=40&lines=Let%27s+Build+Something+Amazing;Together!" alt="Contact Typing" />
</div>

<div align="center">
  <a href="https://linkedin.com/in/guillermoastorgacalvo">
    <img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  <a href="https://github.com/GuillermoAstorgaCalvo">
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

<div align="center">
  <img src="https://komarev.com/ghpvc/?username=GuillermoAstorgaCalvo&style=flat-square&color=58A6FF" alt="Profile Views" />
  <br>
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=GuillermoAstorgaCalvo&theme=react-dark&hide_border=true&bg_color=0D1117&color=58A6FF&line=58A6FF&point=58A6FF" alt="Activity Graph" />
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
    print("🔄 Generating enhanced dynamic README...")
    
    # Load analytics data
    data = load_analytics_data()
    
    # Generate enhanced README content
    content = generate_enhanced_readme(data)
    
    # Always write to project root
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    readme_path = os.path.join(root_dir, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Enhanced README.md generated successfully!")
    print(f"📊 Data source: analytics_history.json")
    print(f"📅 Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"🎨 Features: Modern design, dynamic stats, project showcase, tech stack")

if __name__ == "__main__":
    main() 
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
            "description": "A modern real estate platform that's changing how people find and manage properties. Built with a focus on user experience and AI-powered features.",
            "tech_stack": ["React", "TypeScript", "TailwindCSS", "Next.js"],
            "features": ["AI Property Matching", "Virtual Tours", "Analytics Dashboard"],
            "status": "🟢 Active Development",
            "url": "https://github.com/guillermo-affiliaction/housing-hub-saas",
            "story": "This project started as a simple property listing site and evolved into a comprehensive SaaS platform. I've learned so much about scaling React applications and integrating AI features."
        },
        "TypeScript Backend": {
            "description": "The backbone of our real estate platform. I designed this microservices architecture to handle everything from user authentication to complex data processing.",
            "tech_stack": ["Node.js", "TypeScript", "PostgreSQL", "Docker"],
            "features": ["REST APIs", "Authentication", "Database Management"],
            "status": "🟢 Active Development",
            "url": "https://github.com/guillermo-affiliaction/backend-housing-hub-saas",
            "story": "Building this backend taught me the importance of clean architecture and how to design APIs that scale. TypeScript has been a game-changer for maintainability."
        },
        "Python AI MCP Backend": {
            "description": "An AI-powered backend that feels like magic. It can understand natural language requests and complete complex tasks automatically.",
            "tech_stack": ["Python", "FastAPI", "OpenAI", "PostgreSQL"],
            "features": ["AI Task Completion", "Natural Language Processing", "MCP Integration"],
            "status": "🟢 Active Development",
            "url": "https://github.com/guillermo-affiliaction/IAbackend-inmoIA",
            "story": "This is where my passion for AI really took off. Seeing the system understand and execute complex requests feels like building the future."
        },
        "FacturaIA": {
            "description": "Automating the tedious task of invoice processing. This AI system can extract data from any invoice format and organize it automatically.",
            "tech_stack": ["Python", "React", "TypeScript", "PostgreSQL"],
            "features": ["OCR Processing", "Data Extraction", "Invoice Management"],
            "status": "🟡 In Development",
            "url": "https://github.com/GuillermoAstorgaCalvo/FacturaIA",
            "story": "This project was born from frustration with manual invoice processing. Sometimes the best solutions come from solving real problems you face daily."
        },
        "Restaurant App": {
            "description": "A complete restaurant management solution that I built from scratch. It handles everything from menu management to order processing.",
            "tech_stack": ["React", "Node.js", "MongoDB", "Express.js"],
            "features": ["Order Management", "Menu System", "Admin Dashboard"],
            "status": "🟢 Live",
            "url": "https://restauranteguillermoastorga.up.railway.app/",
            "story": "This was my first full-stack project that went live. The feeling of seeing real users interact with something you built is incredible."
        }
    }

def generate_hero_section() -> str:
    """Generate authentic hero section with personal touch"""
    return """# 👋 Hey there! I'm Guillermo

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=28&pause=1000&color=58A6FF&center=true&vCenter=true&width=600&height=100&lines=Full-Stack+Developer;AI+Enthusiast;Problem+Solver;Code+Craftsman" alt="Typing SVG" />
</div>

I'm a developer who loves building things that make a difference. Whether it's AI-powered applications, modern web platforms, or elegant solutions to complex problems, I'm always excited to dive into new challenges.

<div align="center">
  <img src="https://img.shields.io/badge/Full--Stack%20Developer-React%20%7C%20Node.js%20%7C%20Python-58A6FF?style=for-the-badge&logo=github&logoColor=white" alt="Full-Stack Developer" />
  <img src="https://img.shields.io/badge/AI%20Enthusiast-Machine%20Learning%20%7C%20NLP-4ECDC4?style=for-the-badge&logo=github&logoColor=white" alt="AI Enthusiast" />
  <img src="https://img.shields.io/badge/Problem%20Solver-Clean%20Code%20%7C%20Best%20Practices-FF6B6B?style=for-the-badge&logo=github&logoColor=white" alt="Problem Solver" />
</div>

---

"""

def generate_about_section() -> str:
    """Generate personal about section"""
    return """## 🚀 What I Do

<div align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=GuillermoAstorgaCalvo&show_icons=true&theme=radical&hide_border=true&bg_color=0D1117&title_color=58A6FF&text_color=8B949E&icon_color=58A6FF&include_all_commits=true&count_private=true" alt="GitHub Stats" />
</div>

### 💼 **My Journey**
I started coding because I wanted to build things that could help people. What began as simple scripts has grown into a passion for creating meaningful applications. I love the challenge of turning complex problems into elegant solutions.

**🔭 Currently working on:** AI-powered real estate platforms and intelligent invoice processing systems  
**🌱 Always learning:** New AI/ML techniques, microservices architecture, and emerging technologies  
**👯 Looking to collaborate on:** Open source projects, innovative SaaS solutions, and anything that pushes the boundaries of what's possible  
**💬 Ask me about:** React, TypeScript, Python, AI/ML, or any tech topic - I love sharing knowledge!  
**📫 Get in touch:** [LinkedIn](https://linkedin.com/in/guillermoastorgacalvo) | [Email](mailto:guillermo.astorga.calvo@gmail.com)

### 🎯 **What I Bring to the Table**
- **Frontend Development**: Building responsive, user-friendly interfaces with React, TypeScript, and modern frameworks
- **Backend Development**: Creating robust APIs and services with Node.js, Python, and microservices architecture
- **AI & ML**: Integrating intelligent features that make applications smarter and more intuitive
- **Database & Cloud**: Designing scalable data solutions and deploying to cloud platforms
- **DevOps**: Streamlining development workflows with CI/CD, automation, and best practices

---

"""

def generate_dynamic_stats_section(data: Dict[str, Any]) -> str:
    """Generate authentic stats section with personal narrative"""
    if not data or not isinstance(data, list) or len(data) == 0:
        return ""
    
    latest_data = data[-1]  # Get the most recent data
    
    stats_badges = []
    if 'total_loc' in latest_data:
        stats_badges.append(f'<img src="https://img.shields.io/badge/📈_Lines_of_Code-{format_number(latest_data["total_loc"])}-58A6FF?style=for-the-badge&logo=github&logoColor=white" alt="Lines of Code" />')
    
    if 'total_commits' in latest_data:
        stats_badges.append(f'<img src="https://img.shields.io/badge/📝_Commits-{format_number(latest_data["total_commits"])}-4ECDC4?style=for-the-badge&logo=github&logoColor=white" alt="Total Commits" />')
    
    if 'total_files' in latest_data:
        stats_badges.append(f'<img src="https://img.shields.io/badge/📁_Files-{format_number(latest_data["total_files"])}-FF6B6B?style=for-the-badge&logo=github&logoColor=white" alt="Total Files" />')
    
    if 'repos_processed' in latest_data:
        stats_badges.append(f'<img src="https://img.shields.io/badge/🏢_Repositories-{latest_data["repos_processed"]}-9C27B0?style=for-the-badge&logo=github&logoColor=white" alt="Repositories" />')
    
    return f"""## 📊 **My Coding Journey**

> 📊 **Real stats from my private enterprise repositories**  
> _Updated automatically every Monday - because consistency matters!_

<!-- Dynamic Stats Overview -->
<div align="center">
  {'  '.join(stats_badges)}
</div>

<!-- GitHub Streak -->
<div align="center">
  <img src="https://streak-stats.demolab.com/?user=GuillermoAstorgaCalvo&theme=radical&hide_border=true&background=0D1117&stroke=58A6FF&ring=58A6FF&fire=58A6FF&currStreakNum=8B949E&sideNums=8B949E&currStreakLabel=8B949E&sideLabels=8B949E&dates=8B949E" alt="GitHub Streak" />
</div>

These numbers represent more than just code - they're the result of countless hours solving problems, learning new technologies, and building things that matter. Every line of code tells a story of growth and discovery.

---

"""

def generate_projects_section() -> str:
    """Generate authentic projects section with personal stories"""
    projects = get_project_descriptions()
    
    content = """## 🚀 **Projects That Matter**

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=20&pause=1000&color=58A6FF&center=true&vCenter=true&width=500&height=50&lines=Innovative+SaaS+Solutions;AI-Powered+Applications;Modern+Web+Platforms" alt="Projects Typing" />
</div>

Here are some projects I'm particularly proud of. Each one taught me something valuable and pushed me to grow as a developer.

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

**The Story:** {project_info['story']}

**🔗 [View Project]({project_info['url']})**

---
"""
    
    return content

def generate_tech_stack_section() -> str:
    """Generate authentic tech stack section"""
    return """## 🛠️ **Technologies I Love**

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=18&pause=1000&color=58A6FF&center=true&vCenter=true&width=400&height=40&lines=Modern+Technologies;Best+Practices;Clean+Code" alt="Tech Stack Typing" />
</div>

I believe in using the right tool for the job. Here are the technologies I've grown comfortable with and continue to explore:

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
    """Generate authentic experience section"""
    return """## 💼 **Experience & Growth**

### **🎯 What I Focus On**
I specialize in building full-stack applications that solve real problems. My approach combines modern development practices with a focus on user experience and scalability. I love working with AI and finding ways to make applications more intelligent and intuitive.

### **🏆 What I've Achieved**
- **Built scalable SaaS platforms** that handle real user traffic and data
- **Integrated AI features** that actually improve user experience
- **Maintained high code quality** across multiple enterprise projects
- **Learned to balance** rapid development with long-term maintainability

### **📈 My Growth Journey**
- **Started with simple scripts** and grew into complex applications
- **Learned TypeScript** and never looked back - it's been a game-changer
- **Explored AI/ML** and discovered how powerful it can be when done right
- **Embraced DevOps** practices that make development more efficient

The numbers in my stats aren't just metrics - they represent real problems solved, features built, and lessons learned. Every commit tells a story of growth and discovery.

---

"""

def generate_contact_section() -> str:
    """Generate authentic contact section"""
    return """## 🌟 **Let's Connect**

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=18&pause=1000&color=58A6FF&center=true&vCenter=true&width=400&height=40&lines=Let%27s+Build+Something+Amazing;Together!" alt="Contact Typing" />
</div>

I'm always excited to connect with fellow developers, discuss interesting projects, or explore new opportunities. Whether you want to collaborate on something cool, ask about my projects, or just say hello - I'd love to hear from you!

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
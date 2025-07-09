# 📊 Dynamic README Generation System

## 🎯 **Overview**

This system automatically generates your GitHub profile README from analytics data collected from your private repositories. The README is **dynamically updated** every Monday via GitHub Actions, ensuring it always reflects your current coding activity.

## 🏗️ **Architecture**

### **Data Flow**

```
Private Repositories → GitHub Actions → Analytics Processing → Dynamic README Generation
```

### **Components**

1. **📊 Analytics Collection** (`scripts/process_repo_stats.py`)

   - Collects statistics from each repository
   - Processes language breakdowns
   - Generates per-repository metrics

2. **📈 Data Aggregation** (`scripts/aggregate_stats.py`)

   - Combines data from all repositories
   - Calculates unified statistics
   - Generates comprehensive reports

3. **📝 Dynamic README Generation** (`scripts/generate_readme.py`)

   - Reads analytics data from `analytics_history.json`
   - Generates dynamic badges and tables
   - Creates professional GitHub profile README

4. **🔄 Automated Workflow** (`.github/workflows/update-stats.yml`)
   - Runs every Monday at 3:00 AM UTC
   - Processes all configured repositories
   - Updates README automatically

## 🚀 **Features**

### **Dynamic Stats Badges**

- **Total Lines of Code**: Real-time count from all repositories
- **Total Commits**: Unified commit count across projects
- **Total Files**: Comprehensive file count

### **Repository Breakdown**

- **Expandable table** showing per-repository statistics
- **Distribution percentages** for lines, commits, and files
- **Unified totals** combining all repositories

### **Language Usage Analysis**

- **Top 10 languages** by lines of code
- **Percentage breakdown** of language usage
- **Language emojis** for visual appeal

### **Professional Layout**

- **Consistent theming** with GitHub's dark colors
- **Expandable sections** to keep profile clean
- **Professional badges** and formatting

## 📋 **Configuration**

### **Repository Setup** (`config.yml`)

```yaml
repositories:
  - name: "FacturaIA"
    display_name: "FacturaIA"
    branch: "develop"
    artifact_name: "facturaia-stats"
  - name: "restaurant-app"
    display_name: "Restaurant App"
    branch: "develop"
    artifact_name: "restaurant-app-stats"
```

### **GitHub Secrets**

- `PERSONAL_REPOS_TOKEN`: For personal repositories
- `PRIVATE_REPO_TOKEN`: For organization repositories

## 🔧 **Manual Operations**

### **Regenerate README Manually**

```bash
cd scripts
python regenerate_readme.py
```

### **Test README Generation**

```bash
cd scripts
python generate_readme.py
```

### **View Current Analytics**

```bash
cat analytics_history.json
```

## 📊 **Data Sources**

### **Analytics History** (`analytics_history.json`)

Contains the latest unified statistics:

- Global summary (total lines, commits, files)
- Repository breakdown
- Language usage analysis
- Growth trends (when available)

### **Generated Reports**

- `STATS.md`: Detailed analytics report
- `README.md`: Dynamic GitHub profile README
- `unified_stats.json`: Raw unified statistics

## 🎨 **Customization**

### **Modifying README Template**

Edit `scripts/generate_readme.py` to customize:

- **Layout structure**
- **Badge colors and styling**
- **Section content**
- **Language emojis**

### **Adding New Sections**

1. Add new functions to `generate_readme.py`
2. Call them in `generate_readme_content()`
3. Update the workflow to include new data sources

### **Styling Changes**

- **Color scheme**: Modify badge colors in the script
- **Layout**: Adjust markdown structure
- **Themes**: Change GitHub stats card themes

## 🔄 **Automation**

### **Weekly Updates**

- **Schedule**: Every Monday at 3:00 AM UTC
- **Process**: Collects data from all repositories
- **Output**: Updates README with latest stats

### **Manual Triggers**

- **Workflow dispatch**: Run manually via GitHub Actions
- **Local generation**: Use `regenerate_readme.py`

## 📈 **Scalability**

### **Adding New Repositories**

1. Add repository to `config.yml`
2. Ensure proper token access
3. Run workflow to include new data

### **Performance Optimization**

- **Caching**: Dependencies cached in workflow
- **Parallel processing**: Repositories processed concurrently
- **Efficient data structures**: Optimized JSON processing

## 🛠️ **Troubleshooting**

### **Common Issues**

**README not updating**

- Check GitHub Actions workflow status
- Verify `analytics_history.json` exists
- Ensure proper file permissions

**Missing repository data**

- Verify repository access tokens
- Check repository names in config
- Confirm branch names are correct

**Empty statistics**

- Check git-fame installation
- Verify repository cloning
- Review author patterns in config

### **Debug Commands**

```bash
# Check analytics data
cat analytics_history.json | jq '.'

# Test repository processing
cd scripts && python process_repo_stats.py

# Validate README generation
python generate_readme.py
```

## 🎯 **Benefits**

### **Professional Presentation**

- **Dynamic content** that updates automatically
- **Comprehensive statistics** from private repositories
- **Professional styling** with consistent theming

### **Scalable Architecture**

- **Modular design** for easy maintenance
- **Automated updates** via GitHub Actions
- **Extensible system** for new features

### **Data Accuracy**

- **Real-time statistics** from actual code
- **Unified metrics** across all repositories
- **Language breakdown** based on actual usage

---

_This system ensures your GitHub profile always showcases your current coding activity and professional growth._

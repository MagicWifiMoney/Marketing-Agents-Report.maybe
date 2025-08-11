# 🚀 Digital Marketing Agency Sub-Agents System

A comprehensive, modular AI agent system for digital marketing agencies with 8 specialized sub-agents, workflows, templates, and automation capabilities.

## 📁 **Project Structure**

```
marketing-agency/
├── agency-subagents/           # Main agency system
│   ├── prompts/               # Agent prompt files
│   │   ├── seo-strategist.md
│   │   ├── copywriter.md
│   │   ├── conversion-strategist.md
│   │   ├── research-strategist.md
│   │   ├── analyzer.md
│   │   ├── idea-strategist.md
│   │   ├── social-strategist.md
│   │   └── design-creator.md
│   ├── templates/             # Reusable templates
│   │   ├── seo/
│   │   ├── copy/
│   │   ├── conversion/
│   │   ├── reporting/
│   │   └── design/
│   ├── client-data/           # Client-specific data
│   │   ├── client-a/
│   │   └── client-b/
│   ├── workflows/             # Automated workflows
│   │   ├── new-client-onboarding.md
│   │   ├── monthly-reporting.md
│   │   └── campaign-launch.md
│   ├── master-controller.md   # System overview
│   └── prompt-guide.md        # Usage instructions
├── agents/                    # Legacy 3-agent system
└── README.md                  # This file
```

## 🤖 **Active Sub-Agents**

1. **@seo-strategist** - Technical & Local SEO
2. **@copywriter** - All content creation & copywriting
3. **@conversion-strategist** - CRO & Testing
4. **@research-strategist** - Market & competitor analysis
5. **@analyzer** - Data & reporting
6. **@idea-strategist** - Campaigns & creativity
7. **@social-strategist** - Social media management
8. **@design-creator** - Visual design & social media graphics

## 🚀 **Quick Start**

### **1. Basic Usage**
```bash
# Navigate to the project
cd /Users/jacobgiebel/marketing-agency

# View the master controller
cat agency-subagents/master-controller.md

# Use individual agents
@seo-strategist analyze [client-website.com]
@copywriter create landing page for [client]
@analyzer generate monthly report for [client]
```

### **2. Workflow Automation**
```bash
# Start new client onboarding
"Start new client onboarding for [Client Name]"

# Generate monthly reports
"Monthly reporting for all clients"

# Launch campaign
"Campaign ideation for [client]"
```

## 📋 **Key Features**

### **🎯 Specialized Agents**
- Each agent has specific activation commands
- Detailed templates for common tasks
- Integration protocols for collaboration
- Performance metrics and KPIs

### **🔄 Automated Workflows**
- New client onboarding (7-day process)
- Monthly reporting (comprehensive analysis)
- Campaign launch (multi-phase execution)

### **📄 Template Library**
- SEO audit templates
- Content brief templates
- A/B test templates
- Performance report templates
- Social media design templates

### **👥 Client Management**
- Dedicated client data directories
- Brand guidelines storage
- Performance tracking
- Custom templates per client

## 💾 **Backup & Protection**

### **Git Version Control**
```bash
# Check status
git status

# View history
git log --oneline

# Create backup branch
git checkout -b backup-[date]

# Push to remote (if you have GitHub/GitLab)
git remote add origin [your-repo-url]
git push -u origin main
```

### **Cloud Backup Options**
1. **GitHub/GitLab** - Free private repositories
2. **Google Drive** - Sync entire folder
3. **Dropbox** - Automatic backup
4. **iCloud** - Mac integration

### **Local Protection**
- `.gitignore` prevents accidental deletion
- Git tracks all changes
- Multiple backup strategies recommended

## 🔧 **Maintenance**

### **Regular Updates**
```bash
# Check for changes
git status

# Save new changes
git add .
git commit -m "Update: [description]"

# Create backup
git tag backup-v1.0
```

### **System Health Check**
- Verify all agent prompts are accessible
- Test workflow automation triggers
- Update client data regularly
- Review and optimize templates

## 📚 **Documentation**

- **Master Controller**: `agency-subagents/master-controller.md`
- **Prompt Guide**: `agency-subagents/prompt-guide.md`
- **Individual Agent Docs**: `agency-subagents/prompts/`
- **Template Library**: `agency-subagents/templates/`
- **Workflow Docs**: `agency-subagents/workflows/`

## 🛡️ **Protection Strategies**

### **1. Version Control (Git)**
- ✅ **Implemented**: Full Git repository with history
- ✅ **Protected**: `.gitignore` prevents sensitive file deletion
- ✅ **Tracked**: All changes are logged and recoverable

### **2. Multiple Backups**
- **Local**: Git repository on your Mac
- **Cloud**: Push to GitHub/GitLab (recommended)
- **External**: USB drive or external hard drive
- **Sync**: Cloud storage (Google Drive, Dropbox, iCloud)

### **3. File Protection**
- **Read-only copies**: Create backup copies in different locations
- **Archive**: Compress and store in multiple locations
- **Documentation**: Keep usage notes and instructions

## 🚨 **Emergency Recovery**

If you accidentally delete files:

```bash
# Recover from Git
git checkout HEAD -- [filename]

# Recover entire project
git reset --hard HEAD

# View what was deleted
git log --oneline
git show [commit-hash]
```

## 📞 **Support**

- **System Issues**: Check Git history for recent changes
- **Agent Problems**: Review individual agent prompts
- **Workflow Issues**: Check workflow documentation
- **Template Questions**: Review template library

---

**Last Updated**: [Current Date]
**Version**: 1.0
**Status**: ✅ Active and Protected

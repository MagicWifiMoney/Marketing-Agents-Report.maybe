# 🚀 Notion Integration Setup Guide

## Quick Setup (5 minutes)

### Step 1: Get Your Notion API Key
1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Click "New integration"
3. Name it "Marketing Agency Subagents"
4. Select the workspace where you want the databases
5. Copy the "Internal Integration Token" (this is your API key)

### Step 2: Get Your Notion Page ID
1. Open the Notion page where you want to create the databases
2. Copy the URL - it looks like: `https://notion.so/your-workspace/Page-Title-32characterID`
3. The page ID is the last part: `32characterID`

### Step 3: Update Configuration
1. Open `config.env` in this folder
2. Replace `your_notion_api_key_here` with your actual API key
3. Replace `your_notion_page_id_here` with your actual page ID
4. Save the file

### Step 4: Create Databases
```bash
python3 setup_notion.py
```

This will:
- Create all 6 databases in your Notion workspace
- Save the database IDs to `config.env`
- Set up the complete system

### Step 5: Test the Integration
```bash
python3 test_notion_sync.py
```

This will:
- Test the API connection
- Create sample data in your databases
- Verify everything is working

### Step 6: Enable in Web App
1. Copy `config.env` to your main project as `.env`
2. Restart your web app
3. Check "Save to Notion Database" when generating reports

## 🎯 What You'll Get

### 6 Organized Databases:
1. **Clients** - Master client information
2. **Reports & Audits** - All generated reports
3. **Action Items & Tasks** - Trackable tasks with assignments
4. **Research & Market Insights** - Market research and analysis
5. **Content & Creative Assets** - All content pieces and templates
6. **Performance Metrics & KPIs** - Performance tracking

### Automatic Features:
- **Smart categorization** of all report data
- **Automatic linking** between related items
- **Priority-based task management**
- **Searchable insights** with confidence levels
- **Performance tracking** with metrics

## 🔧 Troubleshooting

### "Database ID not found"
- Run `python3 setup_notion.py` to create databases
- Check that `config.env` has the correct database IDs

### "Notion API key invalid"
- Verify your API key in Notion integrations
- Make sure the integration has access to your page

### "Sync failed"
- Check your internet connection
- Verify all required fields are present
- Check Notion API rate limits

## 📱 Next Steps

1. **Customize views** in Notion for your workflow
2. **Set up filters** to organize data by priority, status, etc.
3. **Create templates** for common client types
4. **Train your team** on the new organized system

Your research and files will now be automatically organized, searchable, and actionable in Notion! 🎉

# 🚀 Notion Integration - Complete Setup

## One-Command Setup

Run this single command to set up everything:

```bash
python3 quick_setup.py
```

This will:
1. ✅ Check prerequisites
2. ✅ Guide you through API key setup
3. ✅ Create all 6 Notion databases
4. ✅ Test the integration
5. ✅ Copy configuration to main project
6. ✅ Ready to use!

## Manual Setup (Alternative)

If you prefer to set up manually:

### 1. Get Notion API Key
1. Go to [Notion Integrations](https://notion.so/my-integrations)
2. Create new integration: "Marketing Agency Subagents"
3. Copy the "Internal Integration Token"

### 2. Get Notion Page ID
1. Open the Notion page where you want databases
2. Copy URL: `https://notion.so/workspace/Page-Title-32characterID`
3. The page ID is: `32characterID`

### 3. Update Configuration
```bash
# Edit config.env with your values
nano config.env
```

### 4. Create Databases
```bash
python3 setup_notion.py
```

### 5. Test Integration
```bash
python3 test_notion_sync.py
```

### 6. Copy to Main Project
```bash
cp config.env ../.env
```

## What You Get

### 6 Organized Databases:
- **Clients** - Master client information
- **Reports & Audits** - All generated reports  
- **Action Items & Tasks** - Trackable tasks
- **Research & Market Insights** - Market research
- **Content & Creative Assets** - Content library
- **Performance Metrics & KPIs** - Performance tracking

### Automatic Features:
- **Smart categorization** of all report data
- **Automatic linking** between related items
- **Priority-based task management**
- **Searchable insights** with confidence levels
- **Performance tracking** with metrics

## Usage

### In Web App:
1. Start your web app: `cd ../report-generator/web && python app.py`
2. Check "Save to Notion Database" when generating reports
3. All data automatically syncs to Notion

### Manual Sync:
```python
from notion_helper import NotionHelper
helper = NotionHelper()
results = helper.sync_report_data(report_data)
```

## Troubleshooting

### "Database ID not found"
- Run `python3 setup_notion.py` to create databases

### "Notion API key invalid"
- Verify API key in Notion integrations
- Ensure integration has access to your page

### "Sync failed"
- Check internet connection
- Verify all required fields are present

## Support

If you need help:
1. Check the setup guide: `setup_guide.md`
2. Run the test: `python3 test_notion_sync.py`
3. Check the logs for specific error messages

Your research and files will now be automatically organized, searchable, and actionable in Notion! 🎉

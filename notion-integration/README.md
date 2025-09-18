# Notion Integration for Marketing Agency Subagents

This integration automatically syncs all your research, reports, and action items to Notion in a digestible, organized format.

## 🎯 What This Does

- **Automatically syncs** all generated reports to Notion databases
- **Organizes data** into digestible, searchable formats
- **Tracks action items** with assignments and due dates
- **Stores research insights** with confidence levels and sources
- **Monitors performance metrics** across all clients
- **Creates content assets** library for reuse

## 📊 Database Structure

### 1. **Clients Database**
- Master client information and project status
- Contact details, budgets, and notes
- Links to all related reports and assets

### 2. **Reports & Audits Database**
- All generated reports and analysis documents
- Executive summaries and key findings
- Recommendations and next steps
- Links to source files and generated agents

### 3. **Action Items & Tasks Database**
- Trackable tasks from all reports
- Assigned to specific agents
- Priority levels and due dates
- Expected impact and completion notes

### 4. **Research & Market Insights Database**
- Market research and competitive analysis
- Keyword research and SEO insights
- Industry trends and opportunities
- Confidence levels and source tracking

### 5. **Content & Creative Assets Database**
- All content pieces and templates
- Performance metrics and target keywords
- Creation dates and approval status
- Links to source files

### 6. **Performance Metrics & KPIs Database**
- Track performance across all clients
- Current vs target vs previous values
- Change percentages and status indicators
- Category-based organization

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
cd notion-integration
pip install -r requirements.txt
```

### 2. Get Your Notion API Key
1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Create a new integration
3. Copy the API key
4. Share your Notion page with the integration

### 3. Set Environment Variables
```bash
# Copy the example file
cp env.example .env

# Edit with your actual values
nano .env
```

Required variables:
- `NOTION_API_KEY`: Your Notion integration API key
- `NOTION_PAGE_ID`: ID of the page where databases will be created

### 4. Create Databases
```bash
python setup_notion.py
```

This creates all 6 databases and saves their IDs to your `.env` file.

### 5. Test the Integration
```bash
python test_notion_sync.py
```

## 🔄 How to Use

### Automatic Sync (Recommended)
1. **Enable in Web App**: Check "Save to Notion Database" when generating reports
2. **Automatic Organization**: All data is automatically categorized and linked
3. **Real-time Updates**: New reports instantly appear in Notion

### Manual Sync
```python
from notion_helper import NotionHelper

# Initialize helper
helper = NotionHelper()

# Sync report data
results = helper.sync_report_data(report_data)
print(f"Synced: {results}")
```

### Individual Components
```python
# Add a client
client_id = helper.add_client({
    "client_name": "New Client",
    "business_type": "Local Service",
    "website": "https://example.com",
    "status": "Active"
})

# Add action items
helper.add_action_items([
    {
        "task_title": "Optimize GMB listing",
        "category": "SEO",
        "priority": "High",
        "assigned_agent": "@seo-strategist"
    }
])
```

## 📱 Notion Views & Filters

### Recommended Views

1. **Client Dashboard**
   - Group by: Status
   - Filter: Active clients
   - Sort by: Start Date (newest first)

2. **Action Items Board**
   - Group by: Status
   - Filter: Not Completed
   - Sort by: Due Date

3. **Research Insights**
   - Group by: Insight Type
   - Filter: High Confidence
   - Sort by: Research Date (newest first)

4. **Performance Metrics**
   - Group by: Category
   - Filter: Below Target
   - Sort by: Change % (lowest first)

### Custom Filters

- **High Priority Tasks**: Status = "Not Started" AND Priority = "High"
- **Recent Insights**: Research Date = "Last 30 days"
- **Client Reports**: Report Type = "SEO Audit" AND Status = "Delivered"
- **Overdue Items**: Due Date < Today AND Status ≠ "Completed"

## 🔧 Advanced Configuration

### Custom Database Properties
Edit `notion_database_schema.json` to add custom properties:

```json
{
  "databases": {
    "clients": {
      "properties": {
        "custom_field": {
          "type": "rich_text",
          "name": "Custom Field"
        }
      }
    }
  }
}
```

### Bulk Operations
```python
# Sync multiple reports
for report_file in report_files:
    with open(report_file, 'r') as f:
        report_data = json.load(f)
    helper.sync_report_data(report_data)

# Update multiple action items
helper.update_action_items(action_updates)
```

### Error Handling
```python
try:
    results = helper.sync_report_data(report_data)
except NotionAPIError as e:
    print(f"Notion API error: {e}")
except ValidationError as e:
    print(f"Data validation error: {e}")
```

## 📈 Benefits

### For You
- **Centralized Knowledge**: All research and reports in one place
- **Searchable History**: Find any insight or recommendation instantly
- **Progress Tracking**: See what's been completed and what's pending
- **Client Management**: Complete client history and relationship tracking

### For Clients
- **Transparent Reporting**: Real-time access to their data
- **Actionable Insights**: Clear next steps and priorities
- **Performance Visibility**: Track progress toward goals
- **Collaborative Planning**: Share and discuss findings

### For Your Team
- **Agent Coordination**: See what each agent is working on
- **Knowledge Sharing**: Learn from successful strategies
- **Quality Control**: Review and approve before client delivery
- **Scalable Processes**: Handle more clients with better organization

## 🛠️ Troubleshooting

### Common Issues

1. **"Database ID not found"**
   - Run `python setup_notion.py` to create databases
   - Check `.env` file has correct database IDs

2. **"Notion API key invalid"**
   - Verify API key in Notion integrations
   - Ensure integration has access to your page

3. **"Sync failed"**
   - Check internet connection
   - Verify all required fields are present
   - Check Notion API rate limits

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

helper = NotionHelper()
# Now you'll see detailed logs
```

### Test Individual Components
```bash
python test_notion_sync.py --components
```

## 🔄 Integration with Report Generator

The web app automatically includes Notion sync when you:
1. Check "Save to Notion Database" in the upload form
2. Generate any report (HTML, PDF, or DOCX)
3. All data is automatically organized and linked

## 📚 Next Steps

1. **Set up your Notion workspace** with the databases
2. **Configure your environment** with API keys
3. **Test with sample data** to verify everything works
4. **Start generating reports** with Notion sync enabled
5. **Customize views and filters** for your workflow
6. **Train your team** on the new organized system

Your research and files will now be automatically organized, searchable, and actionable in Notion! 🎉

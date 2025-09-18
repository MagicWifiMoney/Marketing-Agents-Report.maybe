#!/usr/bin/env python3
"""
Notion Integration Helper for Marketing Agency Subagents
Automatically syncs reports, research, and action items to Notion databases
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotionHelper:
    def __init__(self, api_key: str = None, database_ids: Dict[str, str] = None):
        """
        Initialize Notion helper with API key and database IDs
        
        Args:
            api_key: Notion API key (defaults to NOTION_API_KEY env var)
            database_ids: Dict mapping database names to IDs
        """
        self.api_key = api_key or os.getenv('NOTION_API_KEY')
        if not self.api_key:
            raise ValueError("Notion API key required. Set NOTION_API_KEY environment variable.")
        
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # Database IDs - these need to be set after creating databases in Notion
        self.database_ids = database_ids or {
            "clients": os.getenv('NOTION_CLIENTS_DB_ID'),
            "reports": os.getenv('NOTION_REPORTS_DB_ID'),
            "action_items": os.getenv('NOTION_ACTION_ITEMS_DB_ID'),
            "research_insights": os.getenv('NOTION_RESEARCH_DB_ID'),
            "content_assets": os.getenv('NOTION_CONTENT_DB_ID'),
            "performance_metrics": os.getenv('NOTION_METRICS_DB_ID')
        }
    
    def create_database(self, database_name: str, schema: Dict) -> str:
        """
        Create a new database in Notion
        
        Args:
            database_name: Name of the database
            schema: Database schema from notion_database_schema.json
            
        Returns:
            Database ID
        """
        url = f"{self.base_url}/databases"
        
        payload = {
            "parent": {"type": "page_id", "page_id": os.getenv('NOTION_PAGE_ID')},
            "title": [{"type": "text", "text": {"content": schema["name"]}}],
            "description": [{"type": "text", "text": {"content": schema["description"]}}],
            "properties": schema["properties"]
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            database_id = response.json()["id"]
            logger.info(f"Created database '{database_name}' with ID: {database_id}")
            return database_id
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create database '{database_name}': {e}")
            raise
    
    def add_client(self, client_data: Dict[str, Any]) -> str:
        """Add a new client to the clients database"""
        return self._add_page("clients", client_data)
    
    def add_report(self, report_data: Dict[str, Any]) -> str:
        """Add a new report to the reports database"""
        return self._add_page("reports", report_data)
    
    def add_action_items(self, action_items: List[Dict[str, Any]]) -> List[str]:
        """Add multiple action items to the action items database"""
        page_ids = []
        for item in action_items:
            page_id = self._add_page("action_items", item)
            page_ids.append(page_id)
        return page_ids
    
    def add_research_insight(self, insight_data: Dict[str, Any]) -> str:
        """Add a research insight to the research database"""
        return self._add_page("research_insights", insight_data)
    
    def add_content_asset(self, content_data: Dict[str, Any]) -> str:
        """Add a content asset to the content database"""
        return self._add_page("content_assets", content_data)
    
    def add_performance_metric(self, metric_data: Dict[str, Any]) -> str:
        """Add a performance metric to the metrics database"""
        return self._add_page("performance_metrics", metric_data)
    
    def _add_page(self, database_name: str, data: Dict[str, Any]) -> str:
        """Generic method to add a page to any database"""
        database_id = self.database_ids.get(database_name)
        if not database_id:
            raise ValueError(f"Database ID not found for '{database_name}'. Check environment variables.")
        
        url = f"{self.base_url}/pages"
        
        # Convert data to Notion page properties format
        properties = self._convert_to_notion_properties(data)
        
        payload = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            page_id = response.json()["id"]
            logger.info(f"Added page to '{database_name}' database: {page_id}")
            return page_id
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to add page to '{database_name}': {e}")
            raise
    
    def _convert_to_notion_properties(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert data dictionary to Notion page properties format"""
        properties = {}
        
        for key, value in data.items():
            if value is None:
                continue
                
            # Handle different property types
            if key in ["client_name", "report_title", "task_title", "insight_title", "asset_title", "metric_name"]:
                properties[key] = {"title": [{"text": {"content": str(value)}}]}
            elif key in ["business_type", "report_type", "status", "priority", "assigned_agent", "category", "asset_type", "metric_category"]:
                properties[key] = {"select": {"name": str(value)}}
            elif key in ["website", "file_url"]:
                properties[key] = {"url": str(value)}
            elif key in ["start_date", "report_date", "due_date", "research_date", "created_date", "publish_date", "measurement_date"]:
                properties[key] = {"date": {"start": str(value)}}
            elif key in ["monthly_budget", "current_value", "previous_value", "target_value", "change_percentage"]:
                properties[key] = {"number": float(value) if value else 0}
            elif key in ["action_required"]:
                properties[key] = {"checkbox": bool(value)}
            elif key in ["generated_by", "created_by", "tags"]:
                if isinstance(value, list):
                    properties[key] = {"multi_select": [{"name": str(item)} for item in value]}
                else:
                    properties[key] = {"multi_select": [{"name": str(value)}]}
            elif key in ["client", "report"]:
                # Handle relations - these need to be page IDs
                if isinstance(value, str):
                    properties[key] = {"relation": [{"id": value}]}
            else:
                # Default to rich text for other fields
                properties[key] = {"rich_text": [{"text": {"content": str(value)}}]}
        
        return properties
    
    def sync_report_data(self, report_data: Dict[str, Any], client_id: str = None) -> Dict[str, str]:
        """
        Sync a complete report with all its data to Notion
        
        Args:
            report_data: Parsed report data from markdown parser
            client_id: Optional client ID if client already exists
            
        Returns:
            Dict with page IDs for all created entries
        """
        results = {}
        
        try:
            # 1. Add/update client if not provided
            if not client_id:
                client_data = {
                    "client_name": report_data.get("BUSINESS_NAME", "Unknown Client"),
                    "business_type": report_data.get("BUSINESS_TYPE", "Other"),
                    "website": report_data.get("WEBSITE", ""),
                    "location": report_data.get("LOCATION", ""),
                    "status": "Active",
                    "start_date": datetime.now().strftime("%Y-%m-%d"),
                    "notes": f"Added via report sync on {datetime.now().strftime('%Y-%m-%d')}"
                }
                client_id = self.add_client(client_data)
                results["client_id"] = client_id
            
            # 2. Add main report
            report_entry = {
                "report_title": f"{report_data.get('BUSINESS_NAME', 'Client')} - {report_data.get('REPORT_TYPE', 'Marketing Audit')}",
                "client": client_id,
                "report_type": report_data.get("REPORT_TYPE", "Marketing Audit"),
                "report_date": report_data.get("REPORT_DATE", datetime.now().strftime("%Y-%m-%d")),
                "status": "Delivered",
                "priority": "High",
                "executive_summary": report_data.get("HEALTH_SCORE", ""),
                "key_findings": self._format_key_findings(report_data.get("key_findings", [])),
                "recommendations": self._format_opportunities(report_data.get("immediate_opportunities", [])),
                "next_steps": self._format_next_steps(report_data),
                "generated_by": ["@analyzer", "@seo-strategist", "@research-strategist"]
            }
            report_id = self.add_report(report_entry)
            results["report_id"] = report_id
            
            # 3. Add action items
            action_items = self._extract_action_items(report_data)
            if action_items:
                action_item_ids = self.add_action_items(action_items)
                results["action_items"] = action_item_ids
            
            # 4. Add research insights
            insights = self._extract_research_insights(report_data)
            for insight in insights:
                insight["client"] = client_id
                insight_id = self.add_research_insight(insight)
                results.setdefault("insights", []).append(insight_id)
            
            # 5. Add performance metrics
            metrics = self._extract_performance_metrics(report_data)
            for metric in metrics:
                metric["client"] = client_id
                metric_id = self.add_performance_metric(metric)
                results.setdefault("metrics", []).append(metric_id)
            
            logger.info(f"Successfully synced report data for {report_data.get('BUSINESS_NAME', 'Unknown Client')}")
            return results
            
        except Exception as e:
            logger.error(f"Failed to sync report data: {e}")
            raise
    
    def _format_key_findings(self, findings: List[Dict]) -> str:
        """Format key findings for Notion rich text"""
        if not findings:
            return "No key findings available"
        
        formatted = []
        for finding in findings:
            title = finding.get("title", "")
            description = finding.get("description", "")
            formatted.append(f"• **{title}**: {description}")
        
        return "\n".join(formatted)
    
    def _format_opportunities(self, opportunities: List[Dict]) -> str:
        """Format opportunities for Notion rich text"""
        if not opportunities:
            return "No opportunities identified"
        
        formatted = []
        for opp in opportunities:
            title = opp.get("title", "")
            description = opp.get("description", "")
            priority = opp.get("priority", "medium").upper()
            formatted.append(f"• **{title}** ({priority}): {description}")
        
        return "\n".join(formatted)
    
    def _format_next_steps(self, report_data: Dict) -> str:
        """Format next steps from report data"""
        steps = []
        
        # Add quick wins
        quick_wins = report_data.get("quick_wins", [])
        if quick_wins:
            steps.append("**Quick Wins (0-30 days):**")
            for win in quick_wins[:3]:  # Limit to top 3
                steps.append(f"• {win.get('text', '')}")
        
        # Add strategic actions
        strategic = report_data.get("strategic_actions", [])
        if strategic:
            steps.append("\n**Strategic Initiatives (30-90 days):**")
            for action in strategic[:3]:  # Limit to top 3
                steps.append(f"• {action.get('text', '')}")
        
        return "\n".join(steps) if steps else "Next steps to be determined"
    
    def _extract_action_items(self, report_data: Dict) -> List[Dict]:
        """Extract action items from report data"""
        action_items = []
        
        # Extract from various sections
        sections = [
            ("seo_actions", "SEO"),
            ("conversion_actions", "Conversion"),
            ("quick_wins", "Quick Win"),
            ("strategic_actions", "Strategic")
        ]
        
        for section_key, category in sections:
            items = report_data.get(section_key, [])
            for item in items:
                action_items.append({
                    "task_title": item.get("text", "Untitled Task"),
                    "category": category,
                    "priority": "High" if category == "Quick Win" else "Medium",
                    "status": "Not Started",
                    "expected_impact": item.get("expected_impact", "TBD"),
                    "assigned_agent": self._get_agent_for_category(category)
                })
        
        return action_items
    
    def _extract_research_insights(self, report_data: Dict) -> List[Dict]:
        """Extract research insights from report data"""
        insights = []
        
        # SEO keywords as insights
        seo_keywords = report_data.get("seo_keywords", [])
        if seo_keywords:
            keyword_summary = f"Identified {len(seo_keywords)} keyword opportunities"
            insights.append({
                "insight_title": "SEO Keyword Opportunities",
                "insight_type": "Keyword Research",
                "source": "SEO Analysis",
                "research_date": datetime.now().strftime("%Y-%m-%d"),
                "key_findings": keyword_summary,
                "confidence_level": "High",
                "tags": ["SEO", "Keywords"]
            })
        
        # Market opportunities
        opportunities = report_data.get("immediate_opportunities", [])
        if opportunities:
            insights.append({
                "insight_title": "Market Opportunities Analysis",
                "insight_type": "Market Research",
                "source": "Business Analysis",
                "research_date": datetime.now().strftime("%Y-%m-%d"),
                "key_findings": f"Identified {len(opportunities)} immediate opportunities",
                "confidence_level": "High",
                "tags": ["Strategy", "Market"]
            })
        
        return insights
    
    def _extract_performance_metrics(self, report_data: Dict) -> List[Dict]:
        """Extract performance metrics from report data"""
        metrics = []
        
        # Add placeholder metrics - these would be populated with actual data
        base_metrics = [
            {"name": "Website Traffic", "category": "Traffic", "current": 0, "target": 1000},
            {"name": "Conversion Rate", "category": "Conversions", "current": 0, "target": 2.5},
            {"name": "Local Search Rankings", "category": "Local SEO", "current": 0, "target": 3}
        ]
        
        for metric in base_metrics:
            metrics.append({
                "metric_name": metric["name"],
                "metric_category": metric["category"],
                "current_value": metric["current"],
                "target_value": metric["target"],
                "measurement_date": datetime.now().strftime("%Y-%m-%d"),
                "status": "Below Target"
            })
        
        return metrics
    
    def _get_agent_for_category(self, category: str) -> str:
        """Map category to appropriate agent"""
        mapping = {
            "SEO": "@seo-strategist",
            "Conversion": "@conversion-strategist",
            "Quick Win": "@analyzer",
            "Strategic": "@idea-strategist"
        }
        return mapping.get(category, "@analyzer")

def main():
    """Example usage of NotionHelper"""
    # Load database schema
    with open("notion_database_schema.json", "r") as f:
        schema = json.load(f)
    
    # Initialize helper
    helper = NotionHelper()
    
    # Example: Create databases (run once)
    # for db_name, db_schema in schema["databases"].items():
    #     helper.create_database(db_name, db_schema)
    
    # Example: Sync report data
    sample_report_data = {
        "BUSINESS_NAME": "Trailhead Cycling",
        "BUSINESS_TYPE": "Local Service",
        "WEBSITE": "https://www.trailheadcycling.com/",
        "LOCATION": "Champlin & Plymouth, Minnesota",
        "REPORT_TYPE": "Local Business Audit",
        "REPORT_DATE": "2024-01-15",
        "HEALTH_SCORE": "🟢 STRONG - Optimization Opportunities",
        "key_findings": [
            {"title": "Strong Foundation", "description": "Well-structured website with good SEO setup"},
            {"title": "Growth Opportunities", "description": "E-bike market expansion potential"}
        ],
        "immediate_opportunities": [
            {"title": "Multi-Location SEO", "description": "Optimize both GMB listings", "priority": "high"},
            {"title": "E-bike Market Leadership", "description": "Capitalize on growing demand", "priority": "medium"}
        ]
    }
    
    # results = helper.sync_report_data(sample_report_data)
    # print(f"Synced report data: {results}")

if __name__ == "__main__":
    main()

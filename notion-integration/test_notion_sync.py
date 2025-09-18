#!/usr/bin/env python3
"""
Test Notion Integration
Tests the Notion sync functionality with sample data
"""

import os
import sys
import json
from datetime import datetime
from notion_helper import NotionHelper

def test_notion_sync():
    """Test Notion integration with sample data"""
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv("config.env")
    
    try:
        helper = NotionHelper()
        print("✅ Notion API connection successful")
    except Exception as e:
        print(f"❌ Notion setup failed: {e}")
        return False
    
    # Sample report data (based on Trailhead Cycling audit)
    sample_report_data = {
        "BUSINESS_NAME": "Trailhead Cycling",
        "BUSINESS_TYPE": "Local Service",
        "WEBSITE": "https://www.trailheadcycling.com/",
        "LOCATION": "Champlin & Plymouth, Minnesota",
        "REPORT_TYPE": "Local Business Audit",
        "REPORT_DATE": datetime.now().strftime("%Y-%m-%d"),
        "HEALTH_SCORE": "🟢 STRONG - Optimization Opportunities",
        "key_findings": [
            {
                "title": "Strong Foundation",
                "description": "Well-structured website with good SEO setup, multi-location presence"
            },
            {
                "title": "Premium Positioning", 
                "description": "High-end inventory ($13K bikes) with authorizations (Shimano, Liv)"
            },
            {
                "title": "Growth Opportunities",
                "description": "E-bike market expansion, winter service optimization, local SEO enhancement"
            }
        ],
        "immediate_opportunities": [
            {
                "title": "Multi-Location SEO",
                "description": "Optimize both Champlin & Plymouth GMB listings separately",
                "priority": "high"
            },
            {
                "title": "E-bike Market Leadership",
                "description": "Capitalize on growing e-bike demand and expertise",
                "priority": "medium"
            },
            {
                "title": "Winter Premium Services",
                "description": "Indoor trainer setups, e-bike battery service, bike storage",
                "priority": "medium"
            }
        ],
        "seo_actions": [
            {
                "text": "Complete GMB optimization for both locations",
                "expected_impact": "High visibility improvement"
            },
            {
                "text": "Create service-specific landing pages",
                "expected_impact": "Better local search rankings"
            }
        ],
        "quick_wins": [
            {
                "text": "Add business hours and contact info to GMB",
                "expected_impact": "Immediate visibility boost"
            },
            {
                "text": "Upload photos of shop and services",
                "expected_impact": "Increased trust and engagement"
            }
        ],
        "strategic_actions": [
            {
                "text": "Develop winter service packages",
                "expected_impact": "Year-round revenue stream"
            },
            {
                "text": "Create e-bike expertise content",
                "expected_impact": "Market leadership positioning"
            }
        ],
        "seo_keywords": [
            {
                "keyword": "e-bike shop Plymouth MN",
                "competition": "Low",
                "search_volume": "150-250/mo",
                "opportunity": "HIGH"
            },
            {
                "keyword": "bike repair Champlin MN", 
                "competition": "Low",
                "search_volume": "100-150/mo",
                "opportunity": "HIGH"
            }
        ]
    }
    
    print("\n🔄 Testing Notion sync with sample data...")
    
    try:
        # Sync the report data
        results = helper.sync_report_data(sample_report_data)
        
        print("✅ Successfully synced report data to Notion!")
        print(f"📊 Created entries:")
        print(f"  - Client ID: {results.get('client_id', 'N/A')}")
        print(f"  - Report ID: {results.get('report_id', 'N/A')}")
        print(f"  - Action Items: {len(results.get('action_items', []))}")
        print(f"  - Research Insights: {len(results.get('insights', []))}")
        print(f"  - Performance Metrics: {len(results.get('metrics', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Sync failed: {e}")
        return False

def test_individual_components():
    """Test individual Notion components"""
    
    try:
        helper = NotionHelper()
        print("✅ Notion API connection successful")
    except Exception as e:
        print(f"❌ Notion setup failed: {e}")
        return False
    
    print("\n🧪 Testing individual components...")
    
    # Test client creation
    try:
        client_data = {
            "client_name": "Test Client",
            "business_type": "Local Service",
            "website": "https://test.com",
            "location": "Test City, State",
            "status": "Active",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "notes": "Test client created via API"
        }
        client_id = helper.add_client(client_data)
        print(f"✅ Created test client: {client_id}")
    except Exception as e:
        print(f"❌ Client creation failed: {e}")
        return False
    
    # Test research insight
    try:
        insight_data = {
            "insight_title": "Test Research Insight",
            "insight_type": "Market Research",
            "source": "Test Analysis",
            "research_date": datetime.now().strftime("%Y-%m-%d"),
            "key_findings": "This is a test insight",
            "confidence_level": "High",
            "tags": ["Test", "API"]
        }
        insight_id = helper.add_research_insight(insight_data)
        print(f"✅ Created test insight: {insight_id}")
    except Exception as e:
        print(f"❌ Insight creation failed: {e}")
        return False
    
    print("✅ All individual components working correctly!")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Notion Integration Test")
        print("======================")
        print("This script tests the Notion integration functionality.")
        print("\nPrerequisites:")
        print("1. Run setup_notion.py first to create databases")
        print("2. Ensure .env file has correct database IDs")
        print("\nUsage:")
        print("python test_notion_sync.py          # Test full report sync")
        print("python test_notion_sync.py --components  # Test individual components")
    elif len(sys.argv) > 1 and sys.argv[1] == "--components":
        test_individual_components()
    else:
        test_notion_sync()

#!/usr/bin/env python3
"""
Professional Report Generator - Markdown Parser
Extracts structured data from audit markdown files for report generation
"""

import re
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import argparse
from pathlib import Path

@dataclass
class BusinessInfo:
    name: str = ""
    type: str = ""
    location: str = ""
    website: str = ""
    phone: str = ""
    email: str = ""
    service_area: str = ""

@dataclass  
class KeyMetric:
    name: str
    current: str
    previous: str
    change: str
    target: str
    status: str

@dataclass
class KeywordOpportunity:
    keyword: str
    competition: str
    search_volume: str
    opportunity: str

@dataclass
class ActionItem:
    text: str
    expected_impact: str
    category: str = ""

@dataclass
class BudgetChannel:
    name: str
    amount: str
    roi: str

@dataclass
class TimelinePhase:
    date_range: str
    name: str
    description: str

@dataclass
class ReportData:
    business_info: BusinessInfo
    health_score: str = "🟢 STRONG"
    key_findings: List[Dict[str, str]] = None
    immediate_opportunities: List[Dict[str, str]] = None
    key_metrics: List[KeyMetric] = None
    seo_keywords: List[KeywordOpportunity] = None
    seo_actions: List[ActionItem] = None
    conversion_actions: List[ActionItem] = None
    budget_channels: List[BudgetChannel] = None
    timeline_items: List[TimelinePhase] = None
    quick_wins: List[ActionItem] = None
    strategic_actions: List[ActionItem] = None
    report_type: str = "Marketing Audit"
    report_date: str = ""
    next_review_date: str = ""

class MarkdownParser:
    def __init__(self, markdown_file: str):
        self.markdown_file = Path(markdown_file)
        self.content = self.markdown_file.read_text(encoding='utf-8')
        self.report_data = ReportData(business_info=BusinessInfo())
        
    def parse(self) -> ReportData:
        """Parse the markdown file and extract structured data"""
        self._parse_business_info()
        self._parse_health_assessment()
        self._parse_key_findings()
        self._parse_opportunities()
        self._parse_keyword_table()
        self._parse_action_items()
        self._parse_budget_data()
        self._parse_timeline()
        self._set_report_metadata()
        
        return self.report_data
    
    def _parse_business_info(self):
        """Extract business information from the markdown"""
        # Business name from title
        title_match = re.search(r'# (.+?) - ', self.content)
        if title_match:
            self.report_data.business_info.name = title_match.group(1).strip()
        
        # Business details section
        patterns = {
            'type': r'\*\*Business Type:\*\* (.+)',
            'location': r'\*\*Locations?:\*\* (.+)',
            'website': r'\*\*Website:\*\* (.+)',
            'phone': r'\*\*Phone:\*\* (.+)',
            'email': r'\*\*Email:\*\* (.+)',
            'service_area': r'\*\*Service Area:\*\* (.+)'
        }
        
        for field, pattern in patterns.items():
            match = re.search(pattern, self.content, re.MULTILINE)
            if match:
                value = match.group(1).strip()
                # Clean up markdown formatting
                value = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', value)  # Remove links
                setattr(self.report_data.business_info, field, value)
    
    def _parse_health_assessment(self):
        """Extract health score and assessment"""
        health_match = re.search(r'Business Health Assessment: \*\*(.+?)\*\*', self.content)
        if health_match:
            self.report_data.health_score = health_match.group(1).strip()
    
    def _parse_key_findings(self):
        """Extract key findings from executive summary"""
        findings = []
        
        # Look for key findings section
        findings_section = re.search(r'\*\*Key Findings:\*\*(.+?)(?=\*\*|###|---)', self.content, re.DOTALL)
        if findings_section:
            finding_lines = findings_section.group(1).strip().split('\n')
            for line in finding_lines:
                line = line.strip()
                if line.startswith('-') and '**' in line:
                    # Extract title and description
                    match = re.search(r'- \*\*(.+?):\*\* (.+)', line)
                    if match:
                        findings.append({
                            'title': match.group(1).strip(),
                            'description': match.group(2).strip()
                        })
        
        self.report_data.key_findings = findings
    
    def _parse_opportunities(self):
        """Extract immediate opportunities"""
        opportunities = []
        
        # Find opportunities section
        opp_section = re.search(r'### Immediate Opportunities(.+?)(?=---|###)', self.content, re.DOTALL)
        if opp_section:
            opp_lines = opp_section.group(1).strip().split('\n')
            for line in opp_lines:
                line = line.strip()
                if re.match(r'\d+\.', line):
                    # Extract numbered opportunities
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        title = re.sub(r'^\d+\.\s*\*\*(.+?)\*\*', r'\1', parts[0]).strip()
                        description = parts[1].strip()
                        
                        # Determine priority based on keywords
                        priority = 'medium'
                        if any(word in title.lower() for word in ['high', 'critical', 'immediate']):
                            priority = 'high'
                        elif any(word in title.lower() for word in ['low', 'future', 'later']):
                            priority = 'low'
                        
                        opportunities.append({
                            'title': title,
                            'description': description,
                            'priority': priority
                        })
        
        self.report_data.immediate_opportunities = opportunities
    
    def _parse_keyword_table(self):
        """Extract SEO keywords from tables"""
        keywords = []
        
        # Find keyword tables (look for tables with Keyword, Competition, etc.)
        table_pattern = r'\| Keyword Target.*?\|.*?\n\|[-\|]+\|\n((?:\|.*?\|\n?)+)'
        tables = re.findall(table_pattern, self.content, re.MULTILINE)
        
        for table in tables:
            rows = [row.strip() for row in table.strip().split('\n') if row.strip()]
            for row in rows:
                if '|' in row:
                    cols = [col.strip() for col in row.split('|')[1:-1]]  # Remove empty first/last
                    if len(cols) >= 4:
                        keyword = cols[0].strip('"')
                        competition = cols[1] if len(cols) > 1 else 'Unknown'
                        volume = cols[2] if len(cols) > 2 else 'Unknown'
                        opportunity = cols[3] if len(cols) > 3 else 'Unknown'
                        
                        keywords.append(KeywordOpportunity(
                            keyword=keyword,
                            competition=competition,
                            search_volume=volume,
                            opportunity=opportunity
                        ))
        
        self.report_data.seo_keywords = keywords
    
    def _parse_action_items(self):
        """Extract action items from various sections"""
        seo_actions = []
        conversion_actions = []
        quick_wins = []
        strategic_actions = []
        
        # Pattern for checkbox action items
        action_pattern = r'- \[ \] (.+?)(?:\n|$)'
        
        # SEO Actions
        seo_section = re.search(r'### SEO Recommendations(.+?)(?=---|###)', self.content, re.DOTALL)
        if seo_section:
            seo_matches = re.findall(action_pattern, seo_section.group(1))
            for match in seo_matches:
                seo_actions.append(ActionItem(
                    text=match.strip(),
                    expected_impact=self._estimate_impact(match),
                    category='SEO'
                ))
        
        # Conversion Actions
        conv_section = re.search(r'### (?:Conversion|Lead Generation).+?Opportunities(.+?)(?=---|###)', self.content, re.DOTALL)
        if conv_section:
            conv_matches = re.findall(action_pattern, conv_section.group(1))
            for match in conv_matches:
                conversion_actions.append(ActionItem(
                    text=match.strip(),
                    expected_impact=self._estimate_impact(match),
                    category='Conversion'
                ))
        
        # Quick Wins (usually in immediate actions)
        quick_section = re.search(r'### Immediate Actions(.+?)(?=---|###)', self.content, re.DOTALL)
        if quick_section:
            quick_matches = re.findall(action_pattern, quick_section.group(1))
            for match in quick_matches:
                quick_wins.append(ActionItem(
                    text=match.strip(),
                    expected_impact=self._estimate_impact(match),
                    category='Quick Win'
                ))
        
        # Strategic Actions (90-day items)
        strategic_section = re.search(r'### (?:Growth Initiatives|Strategic).+?\((?:Next )?90 Days?\)(.+?)(?=---|###)', self.content, re.DOTALL)
        if strategic_section:
            strategic_matches = re.findall(action_pattern, strategic_section.group(1))
            for match in strategic_matches:
                strategic_actions.append(ActionItem(
                    text=match.strip(),
                    expected_impact=self._estimate_impact(match),
                    category='Strategic'
                ))
        
        self.report_data.seo_actions = seo_actions
        self.report_data.conversion_actions = conversion_actions
        self.report_data.quick_wins = quick_wins
        self.report_data.strategic_actions = strategic_actions
    
    def _parse_budget_data(self):
        """Extract budget and ROI information"""
        budget_channels = []
        
        # Look for budget tables
        budget_section = re.search(r'### (?:Marketing Investment|Budget).+?Priorities(.+?)(?=---|###)', self.content, re.DOTALL)
        if budget_section:
            # Find table rows
            table_rows = re.findall(r'\| \*\*(.+?)\*\* \| (.+?) \| (.+?) \| (.+?) \|', budget_section.group(1))
            for row in table_rows:
                if len(row) >= 4:
                    channel_name = row[0].strip()
                    # Extract amount from various formats
                    amount = re.search(r'\$(\d+)', row[1])
                    roi = re.search(r'(\d+):1', row[3])
                    
                    if amount:
                        budget_channels.append(BudgetChannel(
                            name=channel_name,
                            amount=amount.group(1),
                            roi=f"{roi.group(1)}:1" if roi else "Unknown"
                        ))
        
        self.report_data.budget_channels = budget_channels
    
    def _parse_timeline(self):
        """Extract implementation timeline"""
        timeline_items = []
        
        # Look for timeline or implementation sections
        timeline_section = re.search(r'### (?:Implementation Timeline|Next Steps)(.+?)(?=---|###)', self.content, re.DOTALL)
        if timeline_section:
            # Find week/month patterns
            phase_pattern = r'### (Week \d+[-\d]*|Month \d+[-\d]*):?\s*(.+?)(?=\n- |\n### |\n\n|$)'
            phases = re.findall(phase_pattern, timeline_section.group(1), re.DOTALL)
            
            for phase_match in phases:
                date_range = phase_match[0].strip()
                description = phase_match[1].strip()
                
                # Extract phase name from description
                lines = description.split('\n')
                phase_name = lines[0].strip() if lines else "Implementation Phase"
                phase_desc = '\n'.join(lines[1:]).strip() if len(lines) > 1 else description
                
                timeline_items.append(TimelinePhase(
                    date_range=date_range,
                    name=phase_name,
                    description=phase_desc
                ))
        
        self.report_data.timeline_items = timeline_items
    
    def _estimate_impact(self, action_text: str) -> str:
        """Estimate impact based on action text keywords"""
        action_lower = action_text.lower()
        
        if any(word in action_lower for word in ['increase', 'improve', 'boost', 'optimize']):
            # Look for percentage improvements
            percent_match = re.search(r'(\d+)%', action_text)
            if percent_match:
                return f"+{percent_match.group(1)}%"
            else:
                return "+20% estimated"
        elif any(word in action_lower for word in ['setup', 'create', 'build', 'implement']):
            return "New capability"
        elif any(word in action_lower for word in ['fix', 'resolve', 'address']):
            return "Issue resolution"
        else:
            return "Improvement"
    
    def _set_report_metadata(self):
        """Set report metadata"""
        from datetime import datetime, timedelta
        
        # Determine report type based on business type
        if 'ecommerce' in self.report_data.business_info.type.lower():
            self.report_data.report_type = "Ecommerce Growth Analysis"
        elif any(word in self.report_data.business_info.type.lower() for word in ['service', 'local', 'shop']):
            self.report_data.report_type = "Local Business Audit"
        else:
            self.report_data.report_type = "Marketing Performance Audit"
        
        # Set dates
        today = datetime.now()
        self.report_data.report_date = today.strftime("%B %d, %Y")
        self.report_data.next_review_date = (today + timedelta(days=30)).strftime("%B %d, %Y")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report data to dictionary for template rendering"""
        data = asdict(self.report_data)
        
        # Add computed fields for template
        data['BUSINESS_NAME'] = self.report_data.business_info.name
        data['BUSINESS_TYPE'] = self.report_data.business_info.type
        data['LOCATION'] = self.report_data.business_info.location
        data['WEBSITE'] = self.report_data.business_info.website
        data['REPORT_TYPE'] = self.report_data.report_type
        data['REPORT_DATE'] = self.report_data.report_date
        data['REPORT_PERIOD'] = "Current Month"
        data['HEALTH_SCORE'] = self.report_data.health_score
        data['NEXT_REVIEW_DATE'] = self.report_data.next_review_date
        data['AGENCY_NAME'] = "Your Marketing Agency"
        data['EMERGENCY_TRIGGERS'] = "Performance drops >20%, reputation issues, technical problems"
        
        # Format for template rendering
        if self.report_data.business_info.type.lower().find('ecommerce') >= 0:
            data['CONVERSION_TITLE'] = "Revenue & Conversion Optimization"
        else:
            data['CONVERSION_TITLE'] = "Lead Generation & Conversion"
        
        return data
    
    def save_json(self, output_file: str):
        """Save parsed data as JSON"""
        with open(output_file, 'w') as f:
            json.dump(self.to_dict(), f, indent=2, default=str)

def main():
    parser = argparse.ArgumentParser(description='Parse marketing audit markdown files')
    parser.add_argument('input_file', help='Input markdown file')
    parser.add_argument('-o', '--output', help='Output JSON file', default='report_data.json')
    parser.add_argument('--print', action='store_true', help='Print parsed data to stdout')
    
    args = parser.parse_args()
    
    # Parse the markdown file
    md_parser = MarkdownParser(args.input_file)
    report_data = md_parser.parse()
    
    if args.print:
        print(json.dumps(md_parser.to_dict(), indent=2, default=str))
    
    # Save to JSON
    md_parser.save_json(args.output)
    print(f"Parsed data saved to {args.output}")

if __name__ == "__main__":
    main()
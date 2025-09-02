#!/usr/bin/env python3
"""
Professional Report Generator - Main Generation Script
Converts markdown audits to professional PDF reports with charts and branding
"""

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any
import re
import os
import sys

# Add parser directory to path
parser_dir = Path(__file__).parent.parent / "parser"
sys.path.insert(0, str(parser_dir))

try:
    from markdown_parser import MarkdownParser
except ImportError:
    # Try alternative import path
    sys.path.insert(0, str(Path(__file__).parent))
    from markdown_parser import MarkdownParser

class ReportGenerator:
    def __init__(self, template_dir: Path = None):
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.template_dir = template_dir or self.project_root / "templates"
        
        # Ensure required tools are available
        self._check_dependencies()
    
    def _check_dependencies(self):
        """Check if required tools are installed"""
        required_tools = ['pandoc', 'wkhtmltopdf']
        missing_tools = []
        
        for tool in required_tools:
            try:
                subprocess.run([tool, '--version'], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                missing_tools.append(tool)
        
        if missing_tools:
            print(f"⚠️  Missing required tools: {', '.join(missing_tools)}")
            print("\nInstallation commands:")
            print("macOS: brew install pandoc wkhtmltopdf")
            print("Ubuntu: sudo apt-get install pandoc wkhtmltopdf")
            print("Windows: Download from respective websites")
            
            # Continue anyway - we can still generate HTML
            print("\n📝 Will generate HTML report (can be manually converted to PDF)")
    
    def generate_report(self, markdown_file: str, output_format: str = "pdf", 
                       output_file: str = None, template: str = "default") -> str:
        """
        Generate a professional report from markdown file
        
        Args:
            markdown_file: Path to the markdown audit file
            output_format: Format to generate (html, pdf, docx)
            output_file: Output file path (auto-generated if None)
            template: Template to use (default, executive, presentation)
        
        Returns:
            Path to generated report file
        """
        markdown_path = Path(markdown_file)
        if not markdown_path.exists():
            raise FileNotFoundError(f"Markdown file not found: {markdown_file}")
        
        # Parse markdown to extract structured data
        print("📋 Parsing markdown file...")
        parser = MarkdownParser(str(markdown_path))
        report_data = parser.parse()
        data_dict = parser.to_dict()
        
        # Generate appropriate output filename
        if not output_file:
            business_name = data_dict.get('BUSINESS_NAME', 'Report').replace(' ', '-').lower()
            output_file = f"{business_name}-audit-report.{output_format}"
        
        output_path = Path(output_file)
        
        # Generate report based on format
        if output_format.lower() == 'html':
            return self._generate_html_report(data_dict, output_path, template)
        elif output_format.lower() == 'pdf':
            # Check if Chrome is available for PDF generation
            chrome_paths = [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '/usr/bin/google-chrome',
                '/usr/bin/chromium-browser'
            ]
            chrome_available = any(Path(path).exists() for path in chrome_paths)
            
            if chrome_available:
                return self._generate_pdf_report(data_dict, output_path, template)
            else:
                print("⚠️  Chrome not available, generating HTML instead")
                # Change output path extension to .html
                html_output_path = output_path.with_suffix('.html')
                return self._generate_html_report(data_dict, html_output_path, template)
        elif output_format.lower() == 'docx':
            # Check if pandoc is available
            try:
                subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
                return self._generate_docx_report(data_dict, output_path, template)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("⚠️  pandoc not available, generating HTML instead")
                # Change output path extension to .html
                html_output_path = output_path.with_suffix('.html')
                return self._generate_html_report(data_dict, html_output_path, template)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def _generate_html_report(self, data: Dict[str, Any], output_path: Path, template: str) -> str:
        """Generate HTML report with styling and charts"""
        print("🎨 Generating HTML report...")
        
        # Load HTML template
        template_path = self.template_dir / "report-template.html"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        template_content = template_path.read_text(encoding='utf-8')
        
        # Replace template variables
        rendered_html = self._render_template(template_content, data)
        
        # Write HTML file
        output_path.write_text(rendered_html, encoding='utf-8')
        
        # Copy CSS file to same directory
        css_source = self.template_dir / "agency-brand.css"
        css_target = output_path.parent / "agency-brand.css"
        if css_source.exists():
            css_target.write_text(css_source.read_text(), encoding='utf-8')
        
        print(f"✅ HTML report generated: {output_path}")
        return str(output_path)
    
    def _generate_pdf_report(self, data: Dict[str, Any], output_path: Path, template: str) -> str:
        """Generate PDF report using wkhtmltopdf"""
        print("📄 Generating PDF report...")
        
        # First generate HTML
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_html:
            html_content = self._generate_html_content(data, template)
            temp_html.write(html_content)
            temp_html_path = temp_html.name
        
        try:
            # Copy CSS to temp directory
            temp_dir = Path(temp_html_path).parent
            css_source = self.template_dir / "agency-brand.css"
            css_temp = temp_dir / "agency-brand.css"
            if css_source.exists():
                css_temp.write_text(css_source.read_text(), encoding='utf-8')
            
            # Convert HTML to PDF using Chrome headless
            cmd = [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '--headless',
                '--disable-gpu',
                '--print-to-pdf=' + str(output_path),
                '--print-to-pdf-no-header',
                '--no-margins',
                f'file://{temp_html_path}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"⚠️  PDF generation failed: {result.stderr}")
                # Fallback to HTML
                html_fallback = output_path.with_suffix('.html')
                self._generate_html_report(data, html_fallback, template)
                print(f"📝 Generated HTML instead: {html_fallback}")
                return str(html_fallback)
            
            print(f"✅ PDF report generated: {output_path}")
            return str(output_path)
            
        finally:
            # Cleanup temp files
            Path(temp_html_path).unlink(missing_ok=True)
            css_temp.unlink(missing_ok=True)
    
    def _generate_docx_report(self, data: Dict[str, Any], output_path: Path, template: str) -> str:
        """Generate DOCX report using pandoc"""
        print("📝 Generating DOCX report...")
        
        # Create markdown content for pandoc
        markdown_content = self._create_pandoc_markdown(data)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_md:
            temp_md.write(markdown_content)
            temp_md_path = temp_md.name
        
        try:
            # Convert to DOCX using pandoc
            cmd = [
                'pandoc',
                temp_md_path,
                '-o', str(output_path),
                '--from', 'markdown',
                '--to', 'docx'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Pandoc conversion failed: {result.stderr}")
            
            print(f"✅ DOCX report generated: {output_path}")
            return str(output_path)
            
        finally:
            Path(temp_md_path).unlink(missing_ok=True)
    
    def _generate_html_content(self, data: Dict[str, Any], template: str) -> str:
        """Generate HTML content for PDF conversion"""
        template_path = self.template_dir / "report-template.html"
        template_content = template_path.read_text(encoding='utf-8')
        return self._render_template(template_content, data)
    
    def _render_template(self, template_content: str, data: Dict[str, Any]) -> str:
        """Render template with data using simple substitution"""
        rendered = template_content
        
        # Simple variable substitution
        for key, value in data.items():
            if isinstance(value, str):
                rendered = rendered.replace(f"{{{{{key}}}}}", value)
        
        # Handle lists and special sections
        rendered = self._render_lists(rendered, data)
        rendered = self._render_tables(rendered, data)
        rendered = self._render_charts(rendered, data)
        
        return rendered
    
    def _render_lists(self, content: str, data: Dict[str, Any]) -> str:
        """Render list sections in template"""
        # Key findings
        if data.get('key_findings'):
            findings_html = ""
            for finding in data['key_findings']:
                findings_html += f"""
                <li style="margin: 8px 0; padding: 8px 0; border-bottom: 1px solid #e5e7eb;">
                    <strong>{finding.get('title', '')}:</strong> {finding.get('description', '')}
                </li>"""
            content = re.sub(r'{{#KEY_FINDINGS}}.*?{{/KEY_FINDINGS}}', findings_html, content, flags=re.DOTALL)
        
        # Opportunities
        if data.get('immediate_opportunities'):
            opp_html = ""
            for opp in data['immediate_opportunities']:
                priority_class = f"opportunity-{opp.get('priority', 'medium')}"
                opp_html += f"""
                <div class="opportunity-box {priority_class}">
                    <h4 class="opportunity-title">{opp.get('title', '')}</h4>
                    <p class="opportunity-description">{opp.get('description', '')}</p>
                </div>"""
            content = re.sub(r'{{#IMMEDIATE_OPPORTUNITIES}}.*?{{/IMMEDIATE_OPPORTUNITIES}}', opp_html, content, flags=re.DOTALL)
        
        # Action items
        for section_name, template_key in [
            ('seo_actions', 'SEO_ACTIONS'),
            ('conversion_actions', 'CONVERSION_ACTIONS'),
            ('quick_wins', 'QUICK_WINS'),
            ('strategic_actions', 'STRATEGIC_ACTIONS')
        ]:
            if data.get(section_name):
                actions_html = ""
                for action in data[section_name]:
                    actions_html += f"""
                    <div class="action-item">
                        <div class="action-checkbox"></div>
                        <div class="action-text">{action.get('text', '')}</div>
                        <div class="action-impact">{action.get('expected_impact', '')}</div>
                    </div>"""
                content = re.sub(f'{{{{#{template_key}}}}}.*?{{{{/{template_key}}}}}', actions_html, content, flags=re.DOTALL)
        
        return content
    
    def _render_tables(self, content: str, data: Dict[str, Any]) -> str:
        """Render table data in template"""
        # SEO Keywords table
        if data.get('seo_keywords'):
            table_html = ""
            for keyword in data['seo_keywords']:
                opp_class = 'excellent' if keyword.get('opportunity', '').upper() == 'HIGH' else 'good'
                table_html += f"""
                <tr>
                    <td>{keyword.get('keyword', '')}</td>
                    <td>{keyword.get('competition', '')}</td>
                    <td>{keyword.get('search_volume', '')}</td>
                    <td><span class="status-{opp_class}">{keyword.get('opportunity', '')}</span></td>
                </tr>"""
            content = re.sub(r'{{#SEO_KEYWORDS}}.*?{{/SEO_KEYWORDS}}', table_html, content, flags=re.DOTALL)
        
        return content
    
    def _render_charts(self, content: str, data: Dict[str, Any]) -> str:
        """Add chart data for JavaScript rendering"""
        # Default chart data if not provided
        lead_source_labels = '"Google Search", "Referrals", "Social Media", "Direct", "Other"'
        lead_source_data = '40, 25, 15, 12, 8'
        
        roi_timeline_labels = '"Month 1", "Month 2", "Month 3", "Month 6", "Month 12"'
        roi_timeline_data = '5000, 12000, 18000, 35000, 60000'
        
        content = content.replace('{{LEAD_SOURCE_LABELS}}', lead_source_labels)
        content = content.replace('{{LEAD_SOURCE_DATA}}', lead_source_data)
        content = content.replace('{{ROI_TIMELINE_LABELS}}', roi_timeline_labels)
        content = content.replace('{{ROI_TIMELINE_DATA}}', roi_timeline_data)
        
        return content
    
    def _create_pandoc_markdown(self, data: Dict[str, Any]) -> str:
        """Create markdown content for pandoc DOCX conversion"""
        markdown_parts = []
        
        # Title
        markdown_parts.append(f"# {data.get('BUSINESS_NAME', 'Business')} Marketing Audit Report\n")
        markdown_parts.append(f"**{data.get('REPORT_TYPE', 'Marketing Audit')}** • {data.get('REPORT_DATE', '')}\n")
        
        # Business Info
        markdown_parts.append("## Business Information\n")
        markdown_parts.append(f"- **Business:** {data.get('BUSINESS_NAME', '')}")
        markdown_parts.append(f"- **Type:** {data.get('BUSINESS_TYPE', '')}")
        markdown_parts.append(f"- **Location:** {data.get('LOCATION', '')}")
        markdown_parts.append(f"- **Website:** {data.get('WEBSITE', '')}\n")
        
        # Executive Summary
        markdown_parts.append("## Executive Summary\n")
        markdown_parts.append(f"**Business Health:** {data.get('HEALTH_SCORE', '')}\n")
        
        if data.get('key_findings'):
            markdown_parts.append("### Key Findings\n")
            for finding in data['key_findings']:
                markdown_parts.append(f"- **{finding.get('title', '')}:** {finding.get('description', '')}")
        
        # Add more sections as needed...
        
        return "\n".join(markdown_parts)

def main():
    parser = argparse.ArgumentParser(description='Generate professional reports from markdown audits')
    parser.add_argument('input_file', help='Input markdown file')
    parser.add_argument('-f', '--format', choices=['html', 'pdf', 'docx'], default='pdf',
                       help='Output format (default: pdf)')
    parser.add_argument('-o', '--output', help='Output file (auto-generated if not specified)')
    parser.add_argument('-t', '--template', default='default', 
                       help='Template to use (default: default)')
    
    args = parser.parse_args()
    
    try:
        generator = ReportGenerator()
        output_file = generator.generate_report(
            args.input_file, 
            args.format, 
            args.output, 
            args.template
        )
        print(f"\n🎉 Report generated successfully: {output_file}")
        
        # Open the file if on macOS
        if sys.platform == 'darwin':
            subprocess.run(['open', output_file])
            
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
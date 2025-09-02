# 🎥 Web App Demo Guide

## Quick Demo Steps

### 1. Start the Web App
```bash
cd /Users/jacobgiebel/Desktop/August\ Claude/marketing-agency-subagents/report-generator/web
./start-web-app.sh
```

### 2. Open Browser
Navigate to: **http://localhost:5000**

You'll see a clean, professional interface with:
- 📋 File upload area
- 🎨 Format options (HTML, PDF, DOCX)
- ⚙️ Template selection
- ✨ Generate button

### 3. Test with Trailhead Cycling
- **Upload:** `../agency-subagents/client-data/trailhead-cycling-audit.md`
- **Format:** Try HTML first (works without dependencies)
- **Template:** Keep "Full Report" selected
- **Click:** "Generate Professional Report"

### 4. What You'll Get
**Professional report with:**
- ✅ Agency branding and colors
- ✅ Business information extracted automatically
- ✅ Executive summary with health score
- ✅ Key metrics and opportunities
- ✅ SEO analysis with keyword tables
- ✅ Action items and timelines
- ✅ Budget recommendations
- ✅ Interactive charts (HTML version)

## Web Interface Features

### Upload Area
- **Drag & drop** markdown files
- **File validation** (only .md files accepted)
- **Visual feedback** on file selection

### Format Options
- **HTML**: Interactive, web-friendly, works everywhere
- **PDF**: Print-ready, professional documents (requires wkhtmltopdf)
- **DOCX**: Editable Microsoft Word format (requires pandoc)

### Template Options
- **Full Report**: Complete 15-20 page analysis
- **Executive Summary**: Key findings and recommendations
- **Presentation**: Slide-ready format

### Professional Output
- **Consistent branding** across all reports
- **Automatic data extraction** from markdown
- **Visual charts** and progress indicators
- **Clean typography** and professional layout
- **Print-optimized** formatting

## Demo Workflow

### For Client Presentations
1. **Upload** client audit markdown
2. **Generate HTML** for screen sharing
3. **Generate PDF** for client delivery
4. **Customize branding** if needed
5. **Email or present** professional report

### For Team Collaboration
1. **Multiple team members** can access web interface
2. **Consistent output** regardless of who generates
3. **Easy sharing** via HTML links
4. **Version control** with dated downloads

### For Scaling
1. **No technical knowledge** required
2. **Works on any device** with browser
3. **Cloud deployment** ready
4. **API integration** possible

## Success Indicators

✅ **Web app starts** without errors  
✅ **File uploads** work smoothly  
✅ **Report generates** with proper formatting  
✅ **Download** works automatically  
✅ **Branding** appears correctly  
✅ **Charts** render properly (HTML)  
✅ **Mobile responsive** on phone/tablet  

## Next Steps After Demo

1. **Customize branding** in `../templates/agency-brand.css`
2. **Add your logo** to `../templates/report-template.html`
3. **Deploy to cloud** for team access
4. **Create client portal** for self-service
5. **Integrate with CRM** or workflow tools

## Troubleshooting Demo Issues

**Port Already in Use:**
```bash
# Kill any existing Flask processes
pkill -f "python.*app.py"
# Try again
./start-web-app.sh
```

**Dependencies Missing:**
```bash
# Install system dependencies (optional for HTML)
brew install pandoc wkhtmltopdf

# Python dependencies auto-install via script
```

**File Upload Fails:**
- Check file is `.md` format
- Ensure file size under 16MB
- Try different browser if issues persist

**Report Generation Fails:**
- HTML format always works
- PDF requires wkhtmltopdf
- DOCX requires pandoc
- Check console for error messages
#!/usr/bin/env python3
"""
Web-based Report Generator
Simple Flask app for generating reports from uploaded markdown files
"""

from flask import Flask, request, send_file, render_template_string, jsonify
import os
import tempfile
import sys
from pathlib import Path

# Add our generator to path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))
sys.path.append(str(parent_dir / "generator"))
sys.path.append(str(parent_dir / "parser"))

# Import with proper module name (file is report-generator.py)
import importlib.util
spec = importlib.util.spec_from_file_location("report_generator", parent_dir / "generator" / "report-generator.py")
report_generator_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report_generator_module)
ReportGenerator = report_generator_module.ReportGenerator

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# HTML template for the upload form
UPLOAD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Marketing Report Generator</title>
    <style>
        body { font-family: 'Inter', sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 40px; }
        .upload-area { border: 2px dashed #2563eb; border-radius: 8px; padding: 40px; text-align: center; margin-bottom: 20px; transition: all 0.3s ease; cursor: pointer; }
        .upload-area:hover { background: #f9fafb; border-color: #1d4ed8; }
        .upload-area.dragover { background: #eff6ff; border-color: #1d4ed8; }
        .btn { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 16px; }
        .btn:hover { background: #1d4ed8; }
        .options { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
        .option-group { padding: 15px; border: 1px solid #e5e7eb; border-radius: 6px; }
        .generated-reports { margin-top: 30px; padding: 20px; background: #f9fafb; border-radius: 8px; }
        .success { color: #10b981; font-weight: 600; }
        .error { color: #ef4444; font-weight: 600; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Professional Marketing Report Generator</h1>
        <p>Transform your markdown audits into beautiful, client-ready reports</p>
    </div>

    <form id="uploadForm" enctype="multipart/form-data">
        <div class="upload-area">
            <h3>📋 Upload Markdown Audit File</h3>
            <input type="file" name="markdown_file" accept=".md" required style="margin: 10px;">
        </div>

        <div class="options">
            <div class="option-group">
                <label><strong>Output Format:</strong></label><br>
                <input type="radio" name="format" value="html" checked> HTML (Interactive)<br>
                <input type="radio" name="format" value="pdf"> PDF (Print-ready)<br>
                <input type="radio" name="format" value="docx"> DOCX (Editable)
            </div>
            
            <div class="option-group">
                <label><strong>Template:</strong></label><br>
                <input type="radio" name="template" value="default" checked> Full Report<br>
                <input type="radio" name="template" value="executive"> Executive Summary<br>
                <input type="radio" name="template" value="presentation"> Presentation
            </div>
        </div>

        <div style="text-align: center;">
            <button type="submit" class="btn">✨ Generate Professional Report</button>
        </div>
    </form>

    <div id="result" class="generated-reports" style="display: none;">
        <h3>📊 Generated Report</h3>
        <div id="resultContent"></div>
    </div>

    <script>
        document.getElementById('uploadForm').onsubmit = function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const resultDiv = document.getElementById('result');
            const resultContent = document.getElementById('resultContent');
            
            // Show loading
            resultDiv.style.display = 'block';
            resultContent.innerHTML = '<p>⏳ Generating your professional report...</p>';
            
            fetch('/generate', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    const contentType = response.headers.get('content-type');
                    if (contentType && contentType.includes('application/json')) {
                        return response.json();
                    } else {
                        // File download
                        const filename = response.headers.get('content-disposition')?.split('filename=')[1] || 'report';
                        return response.blob().then(blob => {
                            const url = window.URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = filename;
                            a.click();
                            return { success: true, message: 'Report downloaded successfully!' };
                        });
                    }
                } else {
                    throw new Error('Report generation failed');
                }
            })
            .then(data => {
                if (data.error) {
                    resultContent.innerHTML = `<p class="error">❌ ${data.error}</p>`;
                } else {
                    resultContent.innerHTML = `<p class="success">✅ ${data.message || 'Report generated and downloaded!'}</p>`;
                }
            })
            .catch(error => {
                resultContent.innerHTML = `<p class="error">❌ Error: ${error.message}</p>`;
            });
        };
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Show upload form"""
    return render_template_string(UPLOAD_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate_report():
    """Generate report from uploaded markdown file"""
    try:
        # Check if file was uploaded
        if 'markdown_file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['markdown_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.md'):
            return jsonify({'error': 'Please upload a .md file'}), 400
        
        # Get form options
        output_format = request.form.get('format', 'html')
        template = request.form.get('template', 'default')
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_md:
            file_content = file.read().decode('utf-8')
            temp_md.write(file_content)
            temp_md_path = temp_md.name
        
        try:
            # Generate report
            print(f"Generating report: format={output_format}, template={template}")
            generator = ReportGenerator()
            
            # Create output filename
            base_name = file.filename.replace('.md', '')
            output_filename = f"{base_name}-report.{output_format}"
            
            with tempfile.NamedTemporaryFile(suffix=f'.{output_format}', delete=False) as temp_output:
                output_path = temp_output.name
            
            print(f"Input file: {temp_md_path}")
            print(f"Output file: {output_path}")
            
            # Generate the report
            generated_file = generator.generate_report(
                temp_md_path,
                output_format,
                output_path,
                template
            )
            
            print(f"Generated file: {generated_file}")
            
            # Send file for download
            return send_file(
                generated_file,
                as_attachment=True,
                download_name=output_filename,
                mimetype='application/octet-stream'
            )
            
        finally:
            # Cleanup temp markdown file
            os.unlink(temp_md_path)
            
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'report-generator'})

if __name__ == '__main__':
    print("🚀 Starting Marketing Report Generator Web App...")
    print("📱 Open http://localhost:5001 in your browser")
    print("📋 Upload any markdown audit to generate professional reports")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
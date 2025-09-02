#!/bin/bash

# Professional Report Generator - Main Script
# Converts markdown audit reports to professional PDFs

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
GENERATOR_SCRIPT="$SCRIPT_DIR/generator/report-generator.py"

# Print colored output
print_status() {
    echo -e "${BLUE}ℹ${NC}  $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC}  $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

# Show usage
show_usage() {
    cat << EOF
🚀 Professional Marketing Report Generator

Usage: $0 [OPTIONS] <markdown-file>

OPTIONS:
    -f, --format FORMAT     Output format (html, pdf, docx) [default: pdf]
    -o, --output FILE       Output file name [auto-generated]
    -t, --template TEMPLATE Template to use [default: default]
    -h, --help             Show this help message

EXAMPLES:
    # Generate PDF report
    $0 trailhead-cycling-audit.md
    
    # Generate HTML report with custom output
    $0 -f html -o my-report.html audit.md
    
    # Generate DOCX report
    $0 -f docx client-audit.md

TEMPLATES:
    default     - Full professional report with charts
    executive   - Executive summary focus
    presentation - Presentation-ready format
EOF
}

# Check dependencies
check_dependencies() {
    print_status "Checking dependencies..."
    
    # Check Python 3
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    # Check if generator script exists
    if [ ! -f "$GENERATOR_SCRIPT" ]; then
        print_error "Generator script not found: $GENERATOR_SCRIPT"
        exit 1
    fi
    
    # Make generator script executable
    chmod +x "$GENERATOR_SCRIPT"
    
    # Check optional dependencies
    deps_ok=true
    
    if ! command -v pandoc &> /dev/null; then
        print_warning "pandoc not found - DOCX generation unavailable"
        print_warning "Install with: brew install pandoc (macOS) or apt-get install pandoc (Ubuntu)"
        deps_ok=false
    fi
    
    if ! command -v wkhtmltopdf &> /dev/null; then
        print_warning "wkhtmltopdf not found - PDF generation may fail"
        print_warning "Install with: brew install wkhtmltopdf (macOS) or apt-get install wkhtmltopdf (Ubuntu)"
        deps_ok=false
    fi
    
    if [ "$deps_ok" = true ]; then
        print_success "All dependencies available"
    else
        print_warning "Some optional dependencies missing - HTML generation will work"
    fi
}

# Default values
FORMAT="pdf"
OUTPUT=""
TEMPLATE="default"
INPUT_FILE=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--format)
            FORMAT="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT="$2"
            shift 2
            ;;
        -t|--template)
            TEMPLATE="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        -*)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
        *)
            INPUT_FILE="$1"
            shift
            ;;
    esac
done

# Validate input
if [ -z "$INPUT_FILE" ]; then
    print_error "Input markdown file is required"
    show_usage
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    print_error "Input file not found: $INPUT_FILE"
    exit 1
fi

# Validate format
case $FORMAT in
    html|pdf|docx)
        ;;
    *)
        print_error "Unsupported format: $FORMAT"
        print_error "Supported formats: html, pdf, docx"
        exit 1
        ;;
esac

# Check dependencies
check_dependencies

# Generate report
print_status "Generating $FORMAT report from $INPUT_FILE..."

# Build command
CMD=("python3" "$GENERATOR_SCRIPT" "$INPUT_FILE" "--format" "$FORMAT" "--template" "$TEMPLATE")

if [ -n "$OUTPUT" ]; then
    CMD+=("--output" "$OUTPUT")
fi

# Execute generator
if "${CMD[@]}"; then
    print_success "Report generation completed!"
    
    # If no output specified, try to determine the generated filename
    if [ -z "$OUTPUT" ]; then
        # Extract business name from input file for auto-generated name
        BASENAME=$(basename "$INPUT_FILE" .md)
        GENERATED_FILE="${BASENAME}-audit-report.${FORMAT}"
        
        if [ -f "$GENERATED_FILE" ]; then
            print_status "Generated file: $GENERATED_FILE"
            
            # Open on macOS
            if [[ "$OSTYPE" == "darwin"* ]]; then
                print_status "Opening report..."
                open "$GENERATED_FILE"
            fi
        fi
    fi
else
    print_error "Report generation failed"
    exit 1
fi

# Show next steps
echo ""
print_status "Next steps:"
echo "  • Review the generated report"
echo "  • Customize branding in templates/agency-brand.css"
echo "  • Add your agency logo to the template"
echo "  • Share with client or team"

exit 0
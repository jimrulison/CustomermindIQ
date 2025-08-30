#!/usr/bin/env python3
"""
PDF Generation Script for CustomerMind IQ Training Materials
Converts HTML training materials to professional PDF files
"""

import os
import weasyprint
from pathlib import Path

def generate_pdf_from_html(html_file_path, pdf_file_path):
    """Convert HTML file to PDF using WeasyPrint"""
    try:
        # Read HTML content
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Generate PDF
        html_doc = weasyprint.HTML(string=html_content, base_url=str(Path(html_file_path).parent))
        pdf_doc = html_doc.write_pdf()
        
        # Write PDF to file
        with open(pdf_file_path, 'wb') as f:
            f.write(pdf_doc)
        
        print(f"✅ Successfully generated: {pdf_file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating {pdf_file_path}: {str(e)}")
        return False

def main():
    """Generate all training PDFs"""
    print("🔄 Generating CustomerMind IQ Training PDFs...")
    
    # Create PDFs directory if it doesn't exist
    pdf_dir = Path("/app/pdfs")
    pdf_dir.mkdir(exist_ok=True)
    
    # Define HTML to PDF mappings
    training_materials = [
        {
            "html": "/app/CustomerMind_IQ_Quick_Start_Guide_Professional.html",
            "pdf": "/app/pdfs/CustomerMind_IQ_Quick_Start_Guide.pdf",
            "name": "Quick Start Guide"
        },
        {
            "html": "/app/CustomerMind_IQ_Complete_Training_Manual_Professional.html", 
            "pdf": "/app/pdfs/CustomerMind_IQ_Complete_Training_Manual.pdf",
            "name": "Complete Training Manual"
        },
        {
            "html": "/app/CustomerMind_IQ_Admin_Training_Manual_Professional.html",
            "pdf": "/app/pdfs/CustomerMind_IQ_Admin_Training_Manual.pdf", 
            "name": "Admin Training Manual"
        },
        {
            "html": "/app/CustomerMind_IQ_Training_Portal_Professional.html",
            "pdf": "/app/pdfs/CustomerMind_IQ_Training_Portal.pdf",
            "name": "Training Portal"
        }
    ]
    
    # Generate PDFs
    success_count = 0
    total_count = len(training_materials)
    
    for material in training_materials:
        print(f"\n📄 Processing {material['name']}...")
        
        # Check if HTML file exists
        if not os.path.exists(material['html']):
            print(f"⚠️  HTML file not found: {material['html']}")
            continue
            
        # Generate PDF
        if generate_pdf_from_html(material['html'], material['pdf']):
            success_count += 1
            
            # Get file size for confirmation
            file_size = os.path.getsize(material['pdf'])
            size_mb = file_size / (1024 * 1024)
            print(f"   📦 File size: {size_mb:.2f} MB")
    
    # Summary
    print(f"\n🎉 PDF Generation Complete!")
    print(f"   ✅ Successfully generated: {success_count}/{total_count} PDFs")
    print(f"   📁 PDFs saved to: {pdf_dir}")
    
    # List generated files
    print(f"\n📋 Generated Files:")
    for pdf_file in pdf_dir.glob("*.pdf"):
        size_mb = pdf_file.stat().st_size / (1024 * 1024)
        print(f"   • {pdf_file.name} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    main()
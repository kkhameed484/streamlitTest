import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_test_pdf(output_filename="reportlab_test.pdf"):
    print("Initializing document setup...")
    
    # 1. Page Geometry Configuration (Letter size with 0.5-inch margins)
    margin = 36  # 72 points = 1 inch, so 36 points = 0.5 inch
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )
    
    # Calculate usable content width: Letter width (612) - left (36) - right (36) = 540 points
    usable_width = 540 
    
    # 2. Typography Hierarchy Definition
    styles = getSampleStyleSheet()
    
    # Crucial: Always pair custom fontSize with matching leading to prevent overlapping text
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0F172A'), # Dark slate
        spaceAfter=12
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#334155'), # Charcoal
        spaceAfter=8
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.white
    )

    # 3. Building Content Flow (The Story)
    story = []
    
    # Document Header Banner
    story.append(Paragraph("ReportLab Verification Test", header_style))
    story.append(Paragraph("System Architecture Framework Status Report", body_style))
    story.append(Spacer(1, 15)) # Vertical spacer (15 points)
    
    # Sample Narrative Text Block
    sample_text = (
        "This executable test script validates the baseline environment configuration for "
        "the Python ReportLab implementation. By rendering this multi-page automated canvas, "
        "the engine confirms accurate font metrics mapping, coordinate system matrix math, "
        "and logical programmatic page wrap triggers."
    )
    story.append(Paragraph(sample_text, body_style))
    story.append(Spacer(1, 20))
    
    # 4. Constructing Structured Grid Matrix (Table Layout)
    # Wrapping cells in Paragraphs guarantees text auto-wraps within column constraints
    raw_table_data = [
        ["Component Module", "Target Engine", "Integration Status"],
        ["Canvas Vector Engine", "Core-Graphics v4", "Verified Operational"],
        ["Font TrueType Engine", "Helvetica Native", "Verified Operational"],
        ["Flowable Layout Engine", "PLATYPUS Stream", "Verified Operational"],
        ["Dynamic Memory Buffering", "I/O ByteStream", "Verified Operational"],
        ["Multi-page Spill Over Test", "Page Break Engine", "Forcing Page 2 Transition..."]
    ]
    
    formatted_data = []
    for row_idx, row in enumerate(raw_table_data):
        formatted_row = []
        for cell in row:
            current_style = table_header_style if row_idx == 0 else body_style
            formatted_row.append(Paragraph(cell, current_style))
        formatted_data.append(formatted_row)
        
    # Strictly define concrete column widths summing up exactly to usable_width (540)
    col_widths = [160, 140, 240] 
    
    # Generate long list data to demonstrate automated page cascading boundaries
    # Duplicating rows guarantees the matrix overflows onto page 2 safely
    for _ in range(3): 
        for row in raw_table_data[1:]:
            formatted_data.append([Paragraph(cell, body_style) for cell in row])
            
    # Apply Visual Formatting Matrix Styles
    status_table = Table(formatted_data, colWidths=col_widths, repeatRows=1)
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')), # Header Navy Fill
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]), # Alternating stripes
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#0F172A')), # Bold line below header
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')), # Outer grid wireframe
    ]))
    
    story.append(status_table)
    
    # 5. Build Engine Call
    print("Compiling document flowables into PDF layout...")
    doc.build(story)
    
    # Absolute confirmation path output check
    absolute_path = os.path.abspath(output_filename)
    print(f"\nSuccess! File generated at:\n{absolute_path}")

if __name__ == "__main__":
    create_test_pdf()

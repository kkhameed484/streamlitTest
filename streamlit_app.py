import streamlit as st
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

st.title("📄 PDF Generation Dashboard")
st.write("Click the button below to generate and test your ReportLab PDF layout.")

def generate_pdf_stream():
    # 1. Create an in-memory buffer instead of a local file path
    pdf_buffer = io.BytesIO()
    
    # 2. Initialize the Document Template
    margin = 36  # 0.5 inch margins
    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=letter,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )
    
    # 3. Setup Typography
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1E3A8A'),  # Deep Blue
        spaceAfter=12
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#334155'),  # Dark Slate (Visible text)
        spaceAfter=10
    )
    
    table_header_style = ParagraphStyle(
        'TableHeaderText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.white
    )

    # 4. Assemble the Document Content
    story = []
    
    story.append(Paragraph("System Diagnostic Verification Report", title_style))
    story.append(Spacer(1, 10))
    
    intro_text = (
        "This document confirms that your Streamlit deployment environment is fully "
        "integrated with the ReportLab PDF processing engine. If you can see this text, "
        "your font rendering matrices and paragraph flow architectures are functioning properly."
    )
    story.append(Paragraph(intro_text, body_style))
    story.append(Spacer(1, 15))
    
    # 5. Data Matrix Grid
    raw_data = [
        ["Module Name", "Environment Baseline", "Status Validation"],
        ["Streamlit Cloud Core", "Python Container Runtime", "Verified Operational"],
        ["ReportLab Library", "PLATYPUS Layout Engine", "Verified Operational"],
        ["BytesIO Buffer Stream", "In-Memory Serialization", "Verified Operational"]
    ]
    
    # Wrap text in Paragraph objects to guarantee visible text processing
    formatted_data = []
    for row_idx, row in enumerate(raw_data):
        formatted_row = []
        for cell in row:
            current_style = table_header_style if row_idx == 0 else body_style
            formatted_row.append(Paragraph(cell, current_style))
        formatted_data.append(formatted_row)
        
    # Set explicit visible column widths (totaling 540 points for printable area width)
    explicit_widths = [180, 200, 160]
    
    diagnostic_table = Table(formatted_data, colWidths=explicit_widths)
    diagnostic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),  # Dark header background
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),  # Visible wireframe
    ]))
    
    story.append(diagnostic_table)
    
    # 6. Build the PDF into the buffer memory stream
    doc.build(story)
    
    # Reset buffer cursor pointer back to the start so Streamlit can read it cleanly
    pdf_buffer.seek(0)
    return pdf_buffer

# Trigger PDF compilation
pdf_data = generate_pdf_stream()

# Add a prominent download UI interaction element to Streamlit
st.download_button(
    label="📥 Download Generated PDF Report",
    data=pdf_data,
    file_name="streamlit_reportlab_success.pdf",
    mime="application/pdf"
)

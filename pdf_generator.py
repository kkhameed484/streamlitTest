import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_report_pdf(user_name, report_title, table_data):
    """
    Generates a structured PDF report inside an in-memory buffer.
    Accepts dynamic data arguments directly from the Streamlit UI.
    """
    # 1. Initialize an in-memory binary stream container
    pdf_buffer = io.BytesIO()
    
    # 2. Setup Page Layout Geometry
    margin = 36 # 0.5 inch margins
    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=letter,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )
    
    # 3. Typography Definitions
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=6
    )
    
    meta_style = ParagraphStyle(
        'Metadata',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=15
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#334155')
    )
    
    th_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.white
    )

    story = []
    
    # 4. Inject Dynamic Header Content
    story.append(Paragraph(report_title, title_style))
    story.append(Paragraph(f"Prepared by: {user_name} | Generated automatically via Streamlit Module", meta_style))
    story.append(Spacer(1, 10))
    
    # 5. Build and Layout Data Matrix Grid
    formatted_rows = []
    for row_idx, row in enumerate(table_data):
        formatted_cols = []
        for cell_text in row:
            # Apply distinct style to the header row
            current_style = th_style if row_idx == 0 else body_style
            formatted_cols.append(Paragraph(str(cell_text), current_style))
        formatted_rows.append(formatted_cols)
        
    # Set concrete column widths totaling exactly 540 points
    col_widths = [180, 100, 260]
    
    data_table = Table(formatted_rows, colWidths=col_widths)
    data_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    
    story.append(data_table)
    
    # 6. Finalize Construction and Reset Stream Marker
    doc.build(story)
    pdf_buffer.seek(0)
    
    return pdf_buffer

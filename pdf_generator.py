import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_talent_pdf(actor_name, bio_summary, filmography_data):
    """
    Generates a professional IMDb Talent Profile PDF.
    """
    pdf_buffer = io.BytesIO()
    margin = 36 # 0.5 inch margins
    
    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=letter,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'ActorTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#EAB308'), # IMDb Gold Accent
        spaceAfter=12
    )
    
    body_style = ParagraphStyle(
        'BioBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#334155'),
        spaceAfter=15
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
    
    # 1. Header Sections
    story.append(Paragraph(actor_name, title_style))
    story.append(Paragraph("Verified IMDb Talent Profile & Credits Summary", subtitle_style))
    story.append(Spacer(1, 5))
    
    # 2. Biography Section
    story.append(Paragraph("Biography Overview", ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, leading=18, textColor=colors.HexColor('#1E293B'), spaceAfter=6)))
    story.append(Paragraph(bio_summary, body_style))
    story.append(Spacer(1, 10))
    
    # 3. Filmography Grid Matrix Setup
    story.append(Paragraph("Featured Filmography Credits", ParagraphStyle('H2_2', parent=styles['Heading2'], fontSize=14, leading=18, textColor=colors.HexColor('#1E293B'), spaceAfter=8)))
    
    # Define matrix columns: [Year, Project Title, Credit Role]
    table_rows = [["Release Year", "Production Title / Project Name", "Talent Credit Role"]]
    
    for item in filmography_data:
        table_rows.append([
            str(item.get('year', 'N/A')),
            item.get('title', 'Unknown Project'),
            item.get('role', 'Actor/Actress')
        ])
        
    # Wrap text in Paragraph objects to guarantee visible text auto-wrapping within cells
    formatted_table_data = []
    for row_idx, row in enumerate(table_rows):
        formatted_row = []
        for cell in row:
            current_style = th_style if row_idx == 0 else body_style
            formatted_row.append(Paragraph(str(cell), current_style))
        formatted_table_data.append(formatted_row)
        
    # Standard printable width is 540 points. Break down column allocation:
    col_widths = [100, 290, 150]
    
    credit_table = Table(formatted_table_data, colWidths=col_widths)
    credit_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')), # Slate dark header
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    
    story.append(credit_table)
    
    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer

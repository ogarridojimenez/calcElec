from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def export_history_pdf(entries, filepath):
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        topMargin=20*mm,
        bottomMargin=20*mm,
        leftMargin=20*mm,
        rightMargin=20*mm
    )
    
    story = []
    
    # Custom styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor('#0891b2'),
        spaceAfter=10,
        alignment=TA_LEFT
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        spaceAfter=20
    )
    
    calc_title_style = ParagraphStyle(
        'CalcTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#0e7490'),
        spaceAfter=8,
        borderPadding=10,
        borderWidth=1,
        borderColor=colors.HexColor('#0891b2'),
        backgroundColor=colors.HexColor('#f0fdfa')
    )
    
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4,
        fontName='Helvetica-Bold'
    )
    
    input_key_style = ParagraphStyle(
        'InputKey',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=2
    )
    
    input_value_style = ParagraphStyle(
        'InputValue',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#0f172a')
    )
    
    result_key_style = ParagraphStyle(
        'ResultKey',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#059669'),
        fontName='Helvetica-Bold',
        spaceAfter=2
    )
    
    result_value_style = ParagraphStyle(
        'ResultValue',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#047857'),
        fontName='Helvetica-Bold'
    )
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceBefore=20
    )
    
    # Header
    story.append(Paragraph("⚡ CalcElec", title_style))
    story.append(Paragraph("Calculadora Eléctrica - Historial de Cálculos", subtitle_style))
    story.append(Paragraph(f"Fecha de exportación: {datetime.now().strftime('%d/%m/%Y a las %H:%M')}", subtitle_style))
    story.append(Spacer(1, 10))
    
    # Divider line
    divider_data = [['']]
    divider_table = Table(divider_data, colWidths=[180*mm])
    divider_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#e2e8f0')),
    ]))
    story.append(divider_table)
    story.append(Spacer(1, 15))
    
    for idx, entry in enumerate(entries, 1):
        nombre = entry.get('nombre', 'Sin nombre')
        fecha = entry.get('fecha', '')
        datos = entry.get('datos', {}) or {}
        
        # Calculation header with number
        story.append(Paragraph(f"Cálculo #{idx}: {nombre}", calc_title_style))
        story.append(Paragraph(f"Fecha: {fecha}", input_key_style))
        story.append(Spacer(1, 12))
        
        # Separate INPUTS from RESULTS
        inputs = {}
        resultados = {}
        
        for key, value in datos.items():
            if key.startswith('RESULT_'):
                resultados[key.replace('RESULT_', '')] = value
            elif key in ('valor', 'unidad', 'formula', 'resultado', 'nota'):
                # Treat as results if these common result keys
                resultados[key] = value
            else:
                inputs[key] = value
        
        # If no clear separation, treat all as results
        if not inputs and resultados:
            inputs = {}
        
        # INPUTS section
        if inputs:
            story.append(Paragraph("📥 DATOS DE ENTRADA", section_style))
            story.append(Spacer(1, 6))
            
            # Create table for inputs
            input_data = []
            for key, value in sorted(inputs.items()):
                input_data.append([key, str(value)])
            
            if input_data:
                input_table = Table(input_data, colWidths=[80*mm, 100*mm])
                input_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                    ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#64748b')),
                    ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#0f172a')),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica'),
                    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
                ]))
                story.append(input_table)
        
        story.append(Spacer(1, 15))
        
        # RESULTS section
        if resultados:
            story.append(Paragraph("📊 RESULTADOS", section_style))
            story.append(Spacer(1, 6))
            
            # Create table for results
            result_data = []
            for key, value in sorted(resultados.items()):
                result_data.append([key, str(value)])
            
            if result_data:
                result_table = Table(result_data, colWidths=[80*mm, 100*mm])
                result_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0fdfa')),
                    ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#047857')),
                    ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#065f46')),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (0, -1), 10),
                    ('FONTSIZE', (1, 0), (1, -1), 11),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#a7f3d0')),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#f0fdfa'), colors.HexColor('#d1fae5')]),
                ]))
                story.append(result_table)
        
        # Space between calculations
        story.append(Spacer(1, 20))
        
        # Divider between entries
        if idx < len(entries):
            divider_data2 = [['']]
            divider_table2 = Table(divider_data2, colWidths=[180*mm])
            divider_table2.setStyle(TableStyle([
                ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.HexColor('#cbd5e1')),
            ]))
            story.append(divider_table2)
            story.append(Spacer(1, 15))
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph("— CalcElec | Calculadora Eléctrica Profesional —", footer_style))
    story.append(Paragraph("Generado automáticamente", footer_style))
    
    doc.build(story)
    return filepath
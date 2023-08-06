
from flask import Blueprint, request, Response
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO

api_bp = Blueprint('api', __name__)


def generate_pdf_from_file(file_path, output_path):
    with open(file_path, 'r') as file:
        content = file.read()

    doc = SimpleDocTemplate(output_path, pagesize=landscape(letter))

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.alignment = 1 
    title_style.fontSize = 20 
    title_style.leading = 24 
    code_style = ParagraphStyle('Code', parent=styles['Code'])
    code_style.fontSize = 8
    code_style.fontName = 'Courier'
    elements = []
    elements.append(Paragraph("Dummy CodeQL Analysis Report", title_style))
    elements.append(Spacer(1, 24))  
    elements.append(Paragraph(content, code_style))
    doc.build(elements)


@api_bp.route('/api/pdf', methods=['GET'])
def generate_pdf():
    if not request.method == "GET":
        return "invalid method"
    path = request.args.get("p")
    pdf_buffer = BytesIO()
    generate_pdf_from_file(path, pdf_buffer)
    pdf_buffer.seek(0)
    
    return Response(pdf_buffer, mimetype='application/pdf', headers={
        'Content-Disposition': 'attachment; filename=report.pdf'
    })
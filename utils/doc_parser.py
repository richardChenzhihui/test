import pdfplumber
from docx import Document

def parse_pdf(file_path):
    text_blocks = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_blocks.extend([block.strip() for block in page_text.split('\n\n') if block.strip()])
    return text_blocks

def parse_docx(file_path):
    doc = Document(file_path)
    text_blocks = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return text_blocks

def parse_file(file_path):
    if file_path.lower().endswith('.pdf'):
        return parse_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        return parse_docx(file_path)
    else:
        raise ValueError("Unsupported file type: {}".format(file_path))
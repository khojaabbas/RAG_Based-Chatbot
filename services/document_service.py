from PyPDF2 import PdfReader
from docx import Document


def extract_pdf_text(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def extract_docx_text(file_path):
    doc = Document(file_path)
    text = ""

    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_text(file_path, filename):
    filename = filename.lower()

    if filename.endswith(".pdf"):
        return extract_pdf_text(file_path)

    if filename.endswith(".docx"):
        return extract_docx_text(file_path)

    return ""
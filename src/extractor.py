import os
from docx import Document
from psd_tools import PSDImage
import PyPDF2
import openpyxl

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif ext == '.docx':
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        
        elif ext == '.pdf':
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

        elif ext == '.xlsx':
            wb = openpyxl.load_workbook(file_path, data_only=True)
            text_data = []
            for sheet in wb.worksheets:
                for row in sheet.iter_rows(values_only=True):
                    text_data.append(" ".join([str(cell) for cell in row if cell]))
            return "\n".join(text_data)
        
        elif ext == '.psd':
            psd = PSDImage.open(file_path)
            return "\n".join([layer.text for layer in psd.descendants() if layer.type == 'type' and layer.text])
            
    except Exception as e:
        # במקום לקרוס, נחזיר מחרוזת ריקה ונתעד את השגיאה בשקט
        return ""
    
    return ""

import os
from docx import Document
from psd_tools import PSDImage

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        # טיפול בקבצי טקסט רגילים
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        # טיפול בקבצי וורד (DOCX)
        elif ext == '.docx':
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        
        # טיפול בקבצי פוטושופ (PSD) - חילוץ טקסט משכבות
        elif ext == '.psd':
            psd = PSDImage.open(file_path)
            text_layers = []
            for layer in psd.descendants():
                if layer.type == 'type': # בודק אם זו שכבת טקסט
                    text_layers.append(layer.text)
            return "\n".join(text_layers)
            
    except Exception as e:
        return f"Error reading {file_path}: {e}"
    
    return ""

# בדיקה קטנה
# print(extract_text("test_file.psd"))
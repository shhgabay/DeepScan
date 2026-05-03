import os
from extractor import extract_text  # מייבא את הפונקציה מהקובץ הקודם

def run_search(root_folder, search_term):
    print(f"--- מתחיל חיפוש עבור: '{search_term}' בנתיב: {root_folder} ---")
    
    found_count = 0
    # os.walk עובר על כל העץ של התיקיות
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            
            # חילוץ הטקסט מהקובץ
            content = extract_text(file_path)
            
            # בדיקה אם מילת החיפוש נמצאת בטקסט (בלי קשר לאותיות גדולות/קטנות)
            if search_term.lower() in content.lower():
                print(f"[נמצא!] {file_path}")
                found_count += 1
                
    print(f"--- החיפוש הסתיים. נמצאו {found_count} מופעים. ---")

if __name__ == "__main__":
    # כאן אתה מגדיר את התיקייה לחיפוש ואת המילה
    folder_to_scan = input("הכנס נתיב לתיקייה לחיפוש: ")
    term = input("מה המילה שאתה מחפש? ")
    
    run_search(folder_to_scan, term)

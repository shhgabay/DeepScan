import customtkinter as ctk
from tkinter import filedialog
from bidi.algorithm import get_display
import arabic_reshaper
from extractor import extract_text
import os

def fix_heb(text):
    # פונקציה שהופכת את הטקסט כדי שיוצג נכון ב-RTL
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

class DeepScanApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DeepScan - מנוע חיפוש עמוק")
        self.geometry("600x500")
        ctk.set_appearance_mode("dark")

        # כותרת
        self.label = ctk.CTkLabel(self, text=fix_heb("חיפוש טקסט עמוק"), font=("Arial", 24))
        self.label.pack(pady=20)

        # כפתור בחירת תיקייה
        self.folder_button = ctk.CTkButton(self, text=fix_heb("בחר תיקייה לסריקה"), command=self.browse_folder)
        self.folder_button.pack(pady=10)
        self.folder_path = ""

        # שדה חיפוש
        self.search_entry = ctk.CTkEntry(self, placeholder_text=fix_heb("מה לחפש?"), width=300)
        self.search_entry.pack(pady=10)

        # כפתור חיפוש
        self.search_button = ctk.CTkButton(self, text=fix_heb("התחל חיפוש"), command=self.start_search)
        self.search_button.pack(pady=10)

        # אזור תוצאות
        self.results_box = ctk.CTkTextbox(self, width=500, height=200)
        self.results_box.pack(pady=20)

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory()
        
    def start_search(self):
        term = self.search_entry.get()
        if not self.folder_path or not term:
            self.results_box.insert("insert", fix_heb("שגיאה: בחר תיקייה ומילת חיפוש") + "\n")
            return

        self.results_box.delete("0.0", "end")
        self.results_box.insert("insert", fix_heb(f"מחפש '{term}'...") + "\n")
        
        found_count = 0
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                content = extract_text(file_path)
                if term.lower() in content.lower():
                    self.results_box.insert("insert", f"[V] {file}\n")
                    found_count += 1
        
        self.results_box.insert("insert", "\n" + fix_heb(f"סיום! נמצאו {found_count} מופעים."))

if __name__ == "__main__":
    app = DeepScanApp()
    app.mainloop()
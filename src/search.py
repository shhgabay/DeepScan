import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import subprocess
from extractor import extract_text

# פונקציה פשוטה להיפוך סדר מילים לעברית (RTL)
def fix_heb(text, reverse_words=True):
    if not text: return ""
    words = text.split()
    return " ".join(words[::-1]) if reverse_words else text

class DeepScanApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("DeepScan - מנוע חיפוש עמוק")
        self.geometry("700x650")
        ctk.set_appearance_mode("dark")
        
        # כותרת (כאן לא נהפוך את סדר המילים כי בתמונה היא הופיעה הפוך כשכן הפכנו)
        self.label = ctk.CTkLabel(self, text="מנוע חיפוש טקסט עמוק", font=("Arial Bold", 28))
        self.label.pack(pady=25)

        # שורת כפתורי בחירה
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10)

        self.folder_button = ctk.CTkButton(button_frame, text=fix_heb("בחר תיקייה"), command=self.browse_folder)
        self.folder_button.grid(row=0, column=1, padx=10)

        self.all_pc_button = ctk.CTkButton(button_frame, text=fix_heb("חפש בכל המחשב"), command=self.search_all_pc, fg_color="#555")
        self.all_pc_button.grid(row=0, column=0, padx=10)
        
        self.target_paths = []
        self.path_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.path_label.pack()

        # שדה חיפוש
        self.search_entry = ctk.CTkEntry(self, placeholder_text=fix_heb("מה ברצונך לחפש?"), width=400, justify="right")
        self.search_entry.pack(pady=15)

        self.search_button = ctk.CTkButton(self, text=fix_heb("התחל חיפוש"), command=self.start_search, fg_color="#24a159")
        self.search_button.pack(pady=10)

        # רשימת תוצאות (ניתן ללחוץ)
        self.results_list = [] # נשמור כאן נתיבים מלאים
        self.results_view = ctk.CTkTextbox(self, width=600, height=250, cursor="hand2")
        self.results_view.pack(pady=20)
        self.results_view.bind("<Double-Button-1>", self.open_file) # לחיצה כפולה לפתיחה

        ctk.CTkLabel(self, text=fix_heb("טיפ: לחץ פעמיים על שם קובץ כדי לפתוח אותו"), font=("Arial", 10)).pack()

    def search_all_pc(self):
        # זיהוי כל הכוננים במחשב
        drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]
        self.target_paths = drives
        self.path_label.configure(text=fix_heb("סריקה מוגדרת לכל כונני המחשב"))

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.target_paths = [path]
            self.path_label.configure(text=path)
        
    def start_search(self):
        term = self.search_entry.get()
        if not self.target_paths or not term:
            messagebox.showwarning("שגיאה", fix_heb("יש לבחור יעד ומילת חיפוש"))
            return

        self.results_view.delete("0.0", "end")
        self.results_view.insert("end", fix_heb(f"סורק... אנא המתן").center(50) + "\n\n")
        self.update()
        
        self.results_list = []
        found_count = 0
        
        for path in self.target_paths:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        content = extract_text(file_path)
                        if term.lower() in content.lower():
                            # הוספה לתצוגה ולרשימת הנתיבים
                            self.results_view.insert("end", f"[V] {file}\n")
                            self.results_list.append(file_path)
                            found_count += 1
                            self.update()
                    except: continue
        
        self.results_view.insert("end", f"\n" + fix_heb(f"נמצאו {found_count} תוצאות"))

    def open_file(self, event):
        # פונקציה לפתיחת הקובץ לפי השורה שנלחצה
        try:
            line_index = self.results_view.index("@%d,%d" % (event.x, event.y)).split('.')[0]
            idx = int(line_index) - 3 # התאמה לשורות הפתיחה בתיבה
            if 0 <= idx < len(self.results_list):
                os.startfile(self.results_list[idx])
        except Exception as e:
            print(f"Error opening file: {e}")

if __name__ == "__main__":
    app = DeepScanApp()
    app.mainloop()
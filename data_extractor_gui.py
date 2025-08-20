import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from docx import Document
import pdfplumber
from tabulate import tabulate
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# --------------------- Extractor Functions --------------------- #
def extract_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def extract_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_string()

def extract_from_excel(file_path):
    df = pd.read_excel(file_path)
    return df.to_string()

def extract_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except:
        return ""

# --------------------- Text Processing --------------------- #
def process_text(text, extract_type):
    if extract_type == "word":
        items = text.split()
    elif extract_type == "sentence":
        items = text.split(". ")
    elif extract_type == "paragraph":
        items = text.split("\n\n")
    else:
        items = [text]

    # Build structured output
    structured = []
    for idx, item in enumerate(items, start=1):
        structured.append({
            "ID": idx,
            "Extracted Data": item.strip(),
            "Type": extract_type,
            "Length": len(item),
            "Preview": item[:50] + ("..." if len(item) > 50 else "")
        })
    return structured

# --------------------- GUI --------------------- #
class DataExtractorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Extraction Tool GUI")
        self.master.geometry("650x450")

        # Ensure input and output folders exist
        self.input_folder = "input"
        self.output_folder = "output"
        os.makedirs(self.input_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)

        # Initialize variables
        self.file_path = ""
        self.source_type = ""
        self.extract_type = ""
        self.text = ""
        self.results = []

        # GUI Elements
        tk.Label(master, text="Data Extraction Tool GUI", font=("Arial", 16)).pack(pady=10)
        tk.Button(master, text="Start Extraction", width=25, command=self.start_extraction).pack(pady=10)
        tk.Button(master, text="Exit", width=15, command=master.quit).pack(pady=20)

    # --------------------- GUI Navigation --------------------- #
    def start_extraction(self):
        while True:
            # --------- Source Selection Stage --------- #
            choice = messagebox.askquestion("Source", "Do you want to extract from a file?\nYes = file\nNo = URL")
            if choice == "yes":
                if not self.select_file():
                    return  # Exit if user cancels
            else:
                if not self.enter_url():
                    return  # Exit if user cancels

            # --------- Extraction Type Stage --------- #
            if not self.choose_extract_type():
                continue  # restart extraction type if canceled/invalid

            # --------- Confirmation Stage --------- #
            confirm = self.confirm_selections()
            if confirm == "exit":
                return
            elif confirm == "restart":
                continue
            elif confirm == "modify":
                continue  # allow redoing stages

            # --------- Processing & Preview --------- #
            self.results = process_text(self.text, self.extract_type)
            df = pd.DataFrame(self.results)
            if not self.preview_results(df):
                return  # exit preview canceled

            # --------- Save Stage --------- #
            self.save_results(df)
            # After saving, ask user if they want to restart or exit
            final_choice = messagebox.askquestion("Next Action", "Do you want to extract another file or URL?")
            if final_choice == "yes":
                continue  # restart entire process
            else:
                messagebox.showinfo("Exit", "Exiting program. Goodbye!")
                return

    # --------------------- File/URL Selection --------------------- #
    def select_file(self):
        while True:
            option = messagebox.askyesno("Select File", "Select from input folder?\nYes=input folder, No=browse")
            if option:
                files = os.listdir(self.input_folder)
                if not files:
                    messagebox.showwarning("Empty Folder", "Input folder empty. Browsing instead.")
                    file_path = filedialog.askopenfilename(title="Select file")
                else:
                    file_name = simpledialog.askstring("Input File Name", f"Files available:\n{', '.join(files)}\nEnter file name exactly:")
                    if file_name is None:
                        return False
                    file_path = os.path.join(self.input_folder, file_name)
                    if not os.path.exists(file_path):
                        messagebox.showerror("Error", "Invalid file name. Try again.")
                        continue
            else:
                file_path = filedialog.askopenfilename(title="Select file")
                if not file_path:
                    return False

            self.file_path = file_path
            self.source_type = "file"
            self.load_text()
            if not self.text.strip():
                messagebox.showerror("Error", "Failed to load file. Try again.")
                continue
            messagebox.showinfo("Loaded", f"File loaded: {os.path.basename(self.file_path)}")
            return True

    def enter_url(self):
        while True:
            url = simpledialog.askstring("Enter URL", "Enter the URL:")
            if url is None:
                return False
            self.text = extract_from_url(url)
            if not self.text.strip():
                retry = messagebox.askretrycancel("Error", "Failed to fetch data from URL. Retry?")
                if retry:
                    continue
                else:
                    return False
            self.source_type = "url"
            messagebox.showinfo("Loaded", "Text extracted from URL successfully.")
            return True

    # --------------------- Extraction Type --------------------- #
    def choose_extract_type(self):
        while True:
            extract_type = simpledialog.askstring("Extraction Type", "Choose extraction type (word/sentence/paragraph):")
            if extract_type is None:
                return False
            extract_type = extract_type.lower()
            if extract_type in ["word", "sentence", "paragraph"]:
                self.extract_type = extract_type
                return True
            else:
                messagebox.showerror("Invalid Type", "Choose a valid extraction type.")

    # --------------------- Confirmation --------------------- #
    def confirm_selections(self):
        while True:
            msg = f"Confirm selections:\nSource: {self.source_type}\nExtraction Type: {self.extract_type}\nFile/URL: {os.path.basename(self.file_path) if self.file_path else 'URL'}"
            choice = simpledialog.askstring("Confirm", f"{msg}\n\nOptions: yes=proceed, no=modify, restart=restart, exit=exit")
            if choice is None:
                continue
            choice = choice.lower()
            if choice in ["yes", "y"]:
                return "proceed"
            elif choice in ["no", "modify"]:
                return "modify"
            elif choice == "restart":
                return "restart"
            elif choice == "exit":
                return "exit"

    # --------------------- Load Text --------------------- #
    def load_text(self):
        ext = os.path.splitext(self.file_path)[-1].lower()
        if ext == ".pdf":
            self.text = extract_from_pdf(self.file_path)
        elif ext == ".docx":
            self.text = extract_from_docx(self.file_path)
        elif ext == ".csv":
            self.text = extract_from_csv(self.file_path)
        elif ext in [".xls", ".xlsx"]:
            self.text = extract_from_excel(self.file_path)
        elif ext == ".txt":
            self.text = extract_from_txt(self.file_path)
        else:
            messagebox.showerror("Unsupported File", "Unsupported file type.")
            self.text = ""

    # --------------------- Preview --------------------- #
    def preview_results(self, df):
        preview_window = tk.Toplevel(self.master)
        preview_window.title("Preview Results")
        tk.Label(preview_window, text="Preview of Extracted Data (first 10 rows)").pack(pady=5)
        preview_text = tk.Text(preview_window, height=20, width=100)
        preview_text.pack(padx=10, pady=10)
        preview_text.insert(tk.END, tabulate(df.head(10), headers="keys", tablefmt="grid"))
        return True

    # --------------------- Save --------------------- #
    def save_results(self, df):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        save_name = simpledialog.askstring("Save File", "Enter filename (without extension):")
        if not save_name:
            save_name = "results"
        csv_path = os.path.join(self.output_folder, f"{save_name}_{timestamp}.csv")
        excel_path = os.path.join(self.output_folder, f"{save_name}_{timestamp}.xlsx")
        df.to_csv(csv_path, index=False)
        df.to_excel(excel_path, index=False)
        messagebox.showinfo("Saved", f"Results saved successfully:\nCSV: {csv_path}\nExcel: {excel_path}")

# --------------------- Run GUI --------------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = DataExtractorGUI(root)
    root.mainloop()

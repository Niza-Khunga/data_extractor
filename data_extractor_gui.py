import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from docx import Document
import pdfplumber
import openpyxl
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
        self.master.geometry("600x400")

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
        tk.Button(master, text="Select File", width=20, command=self.select_file).pack(pady=5)
        tk.Button(master, text="Enter URL", width=20, command=self.enter_url).pack(pady=5)
        tk.Button(master, text="Choose Extraction Type", width=25, command=self.choose_extract_type).pack(pady=5)
        tk.Button(master, text="Preview & Save Results", width=25, command=self.preview_and_save).pack(pady=5)
        tk.Button(master, text="Exit", width=15, command=master.quit).pack(pady=20)

    # --------------------- GUI Actions --------------------- #
    def select_file(self):
        # Ask user to browse or select from input folder
        option = messagebox.askyesno("Select File", "Do you want to select from the input folder?\nYes = input folder\nNo = browse file path")
        if option:
            # List files in input folder
            files = os.listdir(self.input_folder)
            if not files:
                messagebox.showwarning("Input Folder Empty", "No files in input folder. Please browse to select a file.")
                self.browse_file()
                return
            # Ask user to type file name
            file_name = simpledialog.askstring("Input File Name", f"Files available:\n{', '.join(files)}\n\nEnter the file name exactly:")
            if not file_name:
                return
            file_path = os.path.join(self.input_folder, file_name)
            if not os.path.exists(file_path):
                messagebox.showerror("File Not Found", "Invalid file name. Please try again.")
                return
        else:
            self.browse_file()
            return

        self.file_path = file_path
        self.source_type = "file"
        self.load_text()
        messagebox.showinfo("File Loaded", f"File loaded successfully:\n{os.path.basename(self.file_path)}")

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select file")
        if not file_path:
            return
        self.file_path = file_path
        self.source_type = "file"
        self.load_text()
        messagebox.showinfo("File Loaded", f"File loaded successfully:\n{os.path.basename(self.file_path)}")

    def enter_url(self):
        url = simpledialog.askstring("Enter URL", "Please enter the URL:")
        if not url:
            return
        self.text = extract_from_url(url)
        if not self.text.strip():
            messagebox.showerror("Error", "Failed to fetch data from URL. Please check the URL and try again.")
            return
        self.source_type = "url"
        messagebox.showinfo("URL Loaded", "Text extracted from URL successfully.")

    def choose_extract_type(self):
        extract_type = simpledialog.askstring("Extraction Type", "Choose extraction type (word/sentence/paragraph):")
        if extract_type and extract_type.lower() in ["word", "sentence", "paragraph"]:
            self.extract_type = extract_type.lower()
            messagebox.showinfo("Extraction Type Selected", f"Extraction type: {self.extract_type}")
        else:
            messagebox.showerror("Invalid Type", "Please choose a valid extraction type.")

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

    def preview_and_save(self):
        if not self.text.strip() or not self.extract_type:
            messagebox.showerror("Missing Data", "Please select a file/URL and extraction type first.")
            return

        self.results = process_text(self.text, self.extract_type)
        df = pd.DataFrame(self.results)

        # Preview first 10 rows
        preview_window = tk.Toplevel(self.master)
        preview_window.title("Preview Results")
        tk.Label(preview_window, text="Preview of Extracted Data (first 10 rows)").pack(pady=5)
        preview_text = tk.Text(preview_window, height=20, width=100)
        preview_text.pack(padx=10, pady=10)
        preview_text.insert(tk.END, tabulate(df.head(10), headers="keys", tablefmt="grid"))

        # Save file
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        save_name = simpledialog.askstring("Save File", f"Enter filename (without extension):\nTimestamp will be added automatically")
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

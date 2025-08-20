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
from tkinter import ttk, filedialog, messagebox

# --- Extractors ---
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
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

# --- Process text depending on choice ---
def process_text(text, extract_type):
    if extract_type == "word":
        return text.split()
    elif extract_type == "sentence":
        return text.split(". ")
    elif extract_type == "paragraph":
        return text.split("\n\n")
    return [text]

# --- GUI Application ---
class DataExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Extraction Tool")
        self.root.geometry("900x600")

        self.input_folder = "input"
        self.output_folder = "output"
        os.makedirs(self.input_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)

        self.source_type = tk.StringVar(value="file")
        self.file_path = tk.StringVar()
        self.url = tk.StringVar()
        self.extract_type = tk.StringVar(value="word")
        self.results = None

        self.create_source_frame()

    # --- Stage 1: Source Selection ---
    def create_source_frame(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Select Source:", font=("Arial", 14)).pack(anchor="w")

        tk.Radiobutton(frame, text="File", variable=self.source_type, value="file").pack(anchor="w")
        tk.Radiobutton(frame, text="URL", variable=self.source_type, value="url").pack(anchor="w")

        tk.Button(frame, text="Select File", command=self.select_file).pack(pady=5)
        tk.Label(frame, text="Or enter URL:").pack(anchor="w")
        tk.Entry(frame, textvariable=self.url, width=50).pack(pady=5)

        tk.Button(frame, text="Next", command=self.confirm_source).pack(pady=10)
        tk.Button(frame, text="Exit", command=self.root.quit).pack(pady=5)

    def select_file(self):
        file = filedialog.askopenfilename(initialdir=self.input_folder)
        if file:
            self.file_path.set(file)

    def confirm_source(self):
        if self.source_type.get() == "file":
            if not self.file_path.get() or not os.path.exists(self.file_path.get()):
                messagebox.showerror("Error", "Please select a valid file.")
                return
        else:
            if not self.url.get().startswith("http"):
                messagebox.showerror("Error", "Please enter a valid URL.")
                return
        self.create_extract_frame()

    # --- Stage 2: Extraction Type ---
    def create_extract_frame(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Select Extraction Type:", font=("Arial", 14)).pack(anchor="w")
        options = ["word", "sentence", "paragraph"]
        ttk.Combobox(frame, textvariable=self.extract_type, values=options, state="readonly").pack(pady=10)

        tk.Button(frame, text="Confirm", command=self.confirm_extraction).pack(pady=5)
        tk.Button(frame, text="Return", command=self.create_source_frame).pack(pady=5)
        tk.Button(frame, text="Restart", command=self.create_source_frame).pack(pady=5)
        tk.Button(frame, text="Exit", command=self.root.quit).pack(pady=5)

    # --- Stage 3: Confirmation ---
    def confirm_extraction(self):
        msg = f"Please confirm your selections:\n\n"
        msg += f"Source Type: {self.source_type.get()}\n"
        if self.source_type.get() == "file":
            msg += f"File: {os.path.basename(self.file_path.get())}\n"
        else:
            msg += f"URL: {self.url.get()}\n"
        msg += f"Extraction Type: {self.extract_type.get()}\n\n"
        msg += "Proceed?"

        response = messagebox.askyesnocancel("Confirm Selections", msg)
        if response is True:
            self.perform_extraction()
        elif response is False:
            self.create_extract_frame()
        else:
            self.create_source_frame()

    # --- Stage 4: Perform Extraction ---
    def perform_extraction(self):
        try:
            if self.source_type.get() == "file":
                ext = os.path.splitext(self.file_path.get())[-1].lower()
                if ext == ".pdf":
                    text = extract_from_pdf(self.file_path.get())
                elif ext == ".docx":
                    text = extract_from_docx(self.file_path.get())
                elif ext == ".csv":
                    text = extract_from_csv(self.file_path.get())
                elif ext in [".xls", ".xlsx"]:
                    text = extract_from_excel(self.file_path.get())
                elif ext == ".txt":
                    text = extract_from_txt(self.file_path.get())
                else:
                    messagebox.showerror("Error", "Unsupported file type.")
                    return
            else:
                text = extract_from_url(self.url.get())
        except Exception as e:
            messagebox.showerror("Error", f"Extraction failed: {str(e)}")
            return

        self.results = process_text(text, self.extract_type.get())
        self.create_output_frame()

    # --- Stage 5: Output Options ---
    def create_output_frame(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Select Output Option:", font=("Arial", 14)).pack(anchor="w")

        tk.Button(frame, text="Display in GUI Table", command=self.display_table).pack(pady=5)
        tk.Button(frame, text="Save to CSV", command=lambda: self.save_results("csv")).pack(pady=5)
        tk.Button(frame, text="Save to Excel", command=lambda: self.save_results("excel")).pack(pady=5)
        tk.Button(frame, text="Return", command=self.create_extract_frame).pack(pady=5)
        tk.Button(frame, text="Restart", command=self.create_source_frame).pack(pady=5)
        tk.Button(frame, text="Exit", command=self.root.quit).pack(pady=5)

    def display_table(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        columns = ("Data",)
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        tree.heading("Data", text="Extracted Data")

        for item in self.results:
            tree.insert("", "end", values=(item,))

        tree.pack(fill="both", expand=True)

        tk.Button(frame, text="Return", command=self.create_output_frame).pack(pady=5)
        tk.Button(frame, text="Restart", command=self.create_source_frame).pack(pady=5)
        tk.Button(frame, text="Exit", command=self.root.quit).pack(pady=5)

    def save_results(self, file_type):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if file_type == "csv":
            filename = f"results_{timestamp}.csv"
            df = pd.DataFrame({"Extracted Data": self.results})
            df.to_csv(os.path.join(self.output_folder, filename), index=False)
        else:
            filename = f"results_{timestamp}.xlsx"
            df = pd.DataFrame({"Extracted Data": self.results})
            df.to_excel(os.path.join(self.output_folder, filename), index=False)

        messagebox.showinfo("Saved", f"Results saved to {filename}")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    app = DataExtractorGUI(root)
    root.mainloop()

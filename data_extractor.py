import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from docx import Document
import pdfplumber
import openpyxl
from tabulate import tabulate

# --- Extractors ---
def extract_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
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

# --- Main program ---
def main():
    print("==== Data Extraction Tool ====")
    source_type = input("Choose source (file/url): ").strip().lower()
    
    if source_type == "file":
        file_path = input("Enter file path: ").strip()
        ext = os.path.splitext(file_path)[-1].lower()
        if ext == ".pdf":
            text = extract_from_pdf(file_path)
        elif ext == ".docx":
            text = extract_from_docx(file_path)
        elif ext == ".csv":
            text = extract_from_csv(file_path)
        elif ext in [".xls", ".xlsx"]:
            text = extract_from_excel(file_path)
        elif ext == ".txt":
            text = extract_from_txt(file_path)
        else:
            print("Unsupported file type.")
            return
    elif source_type == "url":
        url = input("Enter URL: ").strip()
        text = extract_from_url(url)
    else:
        print("Invalid source.")
        return
    
    extract_type = input("Extract (word/sentence/paragraph): ").strip().lower()
    results = process_text(text, extract_type)
    
    # Convert to DataFrame for nice output
    df = pd.DataFrame({"Extracted Data": results})
    print(tabulate(df, headers="keys", tablefmt="grid"))

if __name__ == "__main__":
    main()

import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from docx import Document
import pdfplumber
from tabulate import tabulate
from datetime import datetime
import re

# --- Set up input/output folders ---
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# --- Extractors for different file types ---
def extract_from_pdf(file_path):
    """Extract all text from a PDF file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_from_docx(file_path):
    """Extract all text from a DOCX file."""
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def extract_from_csv(file_path):
    """Convert CSV content to string."""
    df = pd.read_csv(file_path)
    return df.to_string()

def extract_from_excel(file_path):
    """Convert Excel content to string."""
    df = pd.read_excel(file_path)
    return df.to_string()

def extract_from_txt(file_path):
    """Read text file content."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_from_url(url):
    """Extract visible text from a web page."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

# --- Process text based on extraction type ---
def process_text(text, extract_type):
    """
    Splits text based on extraction type:
    - word: splits by whitespace, tracks sentence index
    - sentence: splits by punctuation
    - paragraph: splits by double newline
    """
    if extract_type == "word":
        sentences = re.split(r'(?<=[.!?]) +', text)
        words = []
        word_sentence_idx = []
        for idx, sentence in enumerate(sentences, 1):
            sentence_words = sentence.split()
            words.extend(sentence_words)
            word_sentence_idx.extend([idx]*len(sentence_words))
        return words, word_sentence_idx
    elif extract_type == "sentence":
        sentences = re.split(r'(?<=[.!?]) +', text)
        return sentences, None
    elif extract_type == "paragraph":
        paragraphs = text.split("\n\n")
        paragraphs = [p for p in paragraphs if p.strip()]
        return paragraphs, None
    return [text], None

# --- Helper: generate timestamped filenames ---
def timestamped_filename(input_file_name, extension):
    """Create a unique timestamped filename to avoid overwriting."""
    base_name = os.path.splitext(os.path.basename(input_file_name))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_results_{timestamp}{extension}"

# --- Main program ---
def main():
    print("==== Data Extraction Tool ====")

    while True:  # Outer loop for new file/url
        source_type = input("Choose source (file/url): ").strip().lower()

        # --- File selection options ---
        if source_type == "file":
            print("\nFile selection options:")
            print("1. Enter full file path")
            print("2. Enter file name in 'input/' folder")
            print("3. Pick from list of files in 'input/'")
            file_mode = input("Choose (1/2/3): ").strip()

            if file_mode == "1":
                file_path = input("Enter full file path: ").strip()
            elif file_mode == "2":
                filename = input("Enter file name (e.g., document.pdf): ").strip()
                file_path = os.path.join(INPUT_FOLDER, filename)
            elif file_mode == "3":
                files = os.listdir(INPUT_FOLDER)
                if not files:
                    print(f"❌ No files found in {INPUT_FOLDER}/")
                    continue
                print("\nAvailable files in 'input/':")
                for i, fname in enumerate(files, 1):
                    print(f"{i}. {fname}")
                choice = input("Choose a file number: ").strip()
                if not choice.isdigit() or not (1 <= int(choice) <= len(files)):
                    print("❌ Invalid choice.")
                    continue
                file_path = os.path.join(INPUT_FOLDER, files[int(choice) - 1])
            else:
                print("Invalid choice, try again.")
                continue

            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                continue

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
                continue

        # --- URL extraction ---
        elif source_type == "url":
            url = input("Enter URL: ").strip()
            text = extract_from_url(url)
            file_path = "webpage"
        else:
            print("Invalid source.")
            continue

        while True:  # Inner loop for repeated extraction on same file/url
            extract_type = input("Extract (word/sentence/paragraph): ").strip().lower()
            results, word_sentence_idx = process_text(text, extract_type)

            # --- Build DataFrame with extended attributes ---
            data = []
            for i, content in enumerate(results, 1):
                preview = " ".join(content.split()[:10])  # first 10 words
                row = {
                    "Source": os.path.basename(file_path),
                    "Type": extract_type,
                    "Index": i,
                    "Content": content,
                    "Word Count": len(content.split()),
                    "Character Length": len(content),
                    "Preview": preview
                }
                if extract_type == "word":
                    row["Position"] = i
                    row["Sentence Index"] = word_sentence_idx[i-1]
                data.append(row)

            df = pd.DataFrame(data)

            # --- Output options ---
            print("\nOutput Options:")
            print("1. Display in terminal")
            print("2. Save to CSV")
            print("3. Save to Excel")
            choice = input("Choose (1/2/3): ").strip()

            if choice == "1":
                print(tabulate(df, headers="keys", tablefmt="grid"))
            elif choice == "2":
                out_name = timestamped_filename(file_path, ".csv")
                out_path = os.path.join(OUTPUT_FOLDER, out_name)
                df.to_csv(out_path, index=False)
                print(f"✅ Results saved to {out_path}")
            elif choice == "3":
                out_name = timestamped_filename(file_path, ".xlsx")
                out_path = os.path.join(OUTPUT_FOLDER, out_name)
                df.to_excel(out_path, index=False)
                print(f"✅ Results saved to {out_path}")
            else:
                print("Invalid choice, displaying in terminal by default.")
                print(tabulate(df, headers="keys", tablefmt="grid"))

            # --- Next action ---
            next_action = input(
                "\nWould you like to:\n"
                "1. Extract different data from the same file/url\n"
                "2. Upload a new file/url\n"
                "3. Exit\n"
                "Choose (1/2/3): "
            ).strip()

            if next_action == "1":
                continue
            elif next_action == "2":
                break
            elif next_action == "3":
                print("👋 Exiting program. Goodbye!")
                return
            else:
                print("Invalid choice. Exiting.")
                return

if __name__ == "__main__":
    main()

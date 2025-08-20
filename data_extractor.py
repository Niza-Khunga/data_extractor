import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from docx import Document
import pdfplumber
import openpyxl
from tabulate import tabulate
from datetime import datetime


# --- Ensure input and output folders exist ---
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


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


# --- Helper: timestamped filename based on input file (shorter format) ---
def timestamped_filename(input_file_name, extension):
    base_name = os.path.splitext(os.path.basename(input_file_name))[0]  # Remove path & extension
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Compact format
    return f"{base_name}_results_{timestamp}{extension}"



# --- Main Program ---
def main():
    print("==== Data Extraction Tool ====")

    while True:  # outer loop (restart with new file/url)
        source_type = input("Choose source (file/url): ").strip().lower()

        if source_type == "file":
            print("\nDo you want to:")
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

        elif source_type == "url":
            url = input("Enter URL: ").strip()
            text = extract_from_url(url)
            file_path = "webpage"  # placeholder for naming outputs

        else:
            print("Invalid source.")
            continue

        while True:  # inner loop (reuse same file/url)
            extract_type = input("Extract (word/sentence/paragraph): ").strip().lower()
            results = process_text(text, extract_type)

            df = pd.DataFrame({"Extracted Data": results})

            # --- Output Choice ---
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

            # --- Ask for next action ---
            next_action = input(
                "\nWould you like to:\n"
                "1. Extract different data from the same file/url\n"
                "2. Upload a new file/url\n"
                "3. Exit\n"
                "Choose (1/2/3): "
            ).strip()

            if next_action == "1":
                continue  # reuse same file/url
            elif next_action == "2":
                break  # go back to outer loop
            elif next_action == "3":
                print("👋 Exiting program. Goodbye!")
                return
            else:
                print("Invalid choice. Exiting.")
                return


if __name__ == "__main__":
    main()

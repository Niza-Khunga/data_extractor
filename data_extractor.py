import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from docx import Document
import pdfplumber
from tabulate import tabulate
from datetime import datetime
import re

# --- Setup input/output folders ---
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# --- File extraction functions ---
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

# --- Process text based on extraction type ---
def process_text(text, extract_type):
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

# --- Helper: generate timestamped filename ---
def timestamped_filename(input_file_name, extension):
    base_name = os.path.splitext(os.path.basename(input_file_name))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_results_{timestamp}{extension}"

# --- Main program ---
def main():
    print("==== Data Extraction Tool ====")

    while True:  # Outer loop for source selection
        # --- Source selection stage ---
        while True:
            source_type = input("Choose source (file/url) or type 'exit'/'redo'/'restart': ").strip().lower()
            if source_type == "exit":
                print("👋 Exiting program. Goodbye!")
                return
            elif source_type == "redo":
                continue  # redo this stage
            elif source_type == "restart":
                break  # restart outer loop
            elif source_type in ["file", "url"]:
                break
            print("❌ Invalid source type. Enter 'file' or 'url'.")

        if source_type == "restart":
            continue

        # --- File selection / URL input ---
        while True:
            if source_type == "file":
                while True:
                    print("\nFile selection options:")
                    print("1. Enter full file path")
                    print("2. Enter file name in 'input/' folder")
                    print("3. Pick from list of files in 'input/' folder")
                    file_mode = input("Choose (1/2/3) or 'exit'/'redo'/'restart': ").strip().lower()

                    if file_mode == "exit":
                        print("👋 Exiting program. Goodbye!")
                        return
                    elif file_mode == "redo":
                        continue
                    elif file_mode == "restart":
                        break
                    elif file_mode not in ["1", "2", "3"]:
                        print("❌ Invalid choice. Please select 1, 2, or 3.")
                        continue

                    try:
                        if file_mode == "1":
                            file_path = input("Enter full file path or 'exit'/'redo'/'restart': ").strip()
                            if file_path.lower() == "exit":
                                print("👋 Exiting program. Goodbye!")
                                return
                            elif file_path.lower() == "redo":
                                continue
                            elif file_path.lower() == "restart":
                                break

                        elif file_mode == "2":
                            filename = input("Enter file name in 'input/' folder or 'exit'/'redo'/'restart': ").strip()
                            if filename.lower() == "exit":
                                print("👋 Exiting program. Goodbye!")
                                return
                            elif filename.lower() == "redo":
                                continue
                            elif filename.lower() == "restart":
                                break
                            file_path = os.path.join(INPUT_FOLDER, filename)

                        elif file_mode == "3":
                            files = os.listdir(INPUT_FOLDER)
                            if not files:
                                print(f"❌ No files found in {INPUT_FOLDER}/")
                                continue
                            print("\nAvailable files in 'input/':")
                            for i, fname in enumerate(files, 1):
                                print(f"{i}. {fname}")
                            choice = input("Choose a file number or 'exit'/'redo'/'restart': ").strip()
                            if choice.lower() == "exit":
                                print("👋 Exiting program. Goodbye!")
                                return
                            elif choice.lower() == "redo":
                                continue
                            elif choice.lower() == "restart":
                                break
                            if choice.isdigit() and 1 <= int(choice) <= len(files):
                                file_path = os.path.join(INPUT_FOLDER, files[int(choice)-1])
                            else:
                                print("❌ Invalid choice. Try again.")
                                continue

                        if os.path.exists(file_path):
                            ext = os.path.splitext(file_path)[-1].lower()
                            try:
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
                                    print("❌ Unsupported file type.")
                                    continue
                                break  # valid file and extracted text
                            except Exception as e:
                                print(f"❌ Error reading file: {e}")
                        else:
                            print(f"❌ File not found: {file_path}. Try again.")
                    except Exception as e:
                        print(f"❌ Error: {e}")
                if file_mode.lower() == "restart":
                    break

            elif source_type == "url":
                while True:
                    url = input("Enter URL or 'exit'/'redo'/'restart': ").strip()
                    if url.lower() == "exit":
                        print("👋 Exiting program. Goodbye!")
                        return
                    elif url.lower() == "redo":
                        continue
                    elif url.lower() == "restart":
                        break
                    try:
                        response = requests.get(url)
                        if response.status_code == 200:
                            text = extract_from_url(url)
                            file_path = "webpage"
                            break
                        else:
                            print(f"❌ Unable to reach URL (status {response.status_code}). Try again.")
                    except requests.exceptions.RequestException:
                        print("❌ Invalid URL. Please enter a correct URL.")
                if url.lower() == "restart":
                    break

            if (source_type == "file" and file_mode.lower() == "restart") or (source_type == "url" and url.lower() == "restart"):
                break
            else:
                # Valid selection, move on
                break

        if (source_type == "file" and file_mode.lower() == "restart") or (source_type == "url" and url.lower() == "restart"):
            continue  # back to source selection

        # --- Extraction Type Stage ---
        while True:
            valid_types = ["word", "sentence", "paragraph"]
            while True:
                extract_type = input("Extract (word/sentence/paragraph) or 'exit'/'return'/'redo'/'restart': ").strip().lower()
                if extract_type == "exit":
                    print("👋 Exiting program. Goodbye!")
                    return
                elif extract_type == "redo":
                    continue
                elif extract_type == "return":
                    break  # go back to previous stage (file/url)
                elif extract_type == "restart":
                    break  # go back to choose source
                elif extract_type in valid_types:
                    break
                print(f"❌ Invalid type. Enter one of: {', '.join(valid_types)}")
            if extract_type == "return":
                continue  # back to file/url selection
            elif extract_type == "restart":
                break  # back to source selection
            elif extract_type not in valid_types:
                continue

            # --- Confirmation Stage Before Output ---
            print("\n✅ Current selections:")
            print(f"Source Type: {source_type}")
            if source_type == "file":
                print(f"File: {os.path.basename(file_path)}")
            else:
                print(f"URL: {url}")
            print(f"Extraction Type: {extract_type}")
            confirm = input("\nConfirm selections? (yes/no/exit/restart): ").strip().lower()
            if confirm == "exit":
                print("👋 Exiting program. Goodbye!")
                return
            elif confirm == "restart":
                break  # back to choose source
            elif confirm == "no":
                continue  # allow modifications by returning to extraction type stage
            elif confirm != "yes":
                print("❌ Invalid input. Please type yes, no, restart, or exit.")
                continue

            # --- Process Text ---
            results, word_sentence_idx = process_text(text, extract_type)

            # --- Build structured DataFrame ---
            data = []
            for i, content in enumerate(results, 1):
                preview = " ".join(content.split()[:10])
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

            # --- Output Stage ---
            while True:
                print("\nOutput Options:")
                print("1. Display in terminal")
                print("2. Save to CSV")
                print("3. Save to Excel")
                choice = input("Choose (1/2/3) or 'exit'/'return'/'redo'/'restart': ").strip().lower()
                if choice == "exit":
                    print("👋 Exiting program. Goodbye!")
                    return
                elif choice == "redo":
                    continue
                elif choice == "return":
                    break  # back to extraction type
                elif choice == "restart":
                    break  # back to choose source
                elif choice == "1":
                    print(tabulate(df, headers="keys", tablefmt="grid"))
                    break
                elif choice == "2":
                    out_name = timestamped_filename(file_path, ".csv")
                    out_path = os.path.join(OUTPUT_FOLDER, out_name)
                    df.to_csv(out_path, index=False)
                    print(f"✅ Results saved to {out_path}")
                    break
                elif choice == "3":
                    out_name = timestamped_filename(file_path, ".xlsx")
                    out_path = os.path.join(OUTPUT_FOLDER, out_name)
                    df.to_excel(out_path, index=False)
                    print(f"✅ Results saved to {out_path}")
                    break
                else:
                    print("❌ Invalid choice. Please select 1, 2, 3 or navigation commands.")

            # --- Next Action ---
            print("\nNext Actions:")
            print("1. Extract different data from the same file/url")
            print("2. Upload a new file/url")
            print("3. Exit")
            next_action = input("Choose (1/2/3) or 'restart': ").strip().lower()
            if next_action == "1":
                continue
            elif next_action == "2":
                break
            elif next_action == "3":
                print("👋 Exiting program. Goodbye!")
                return
            elif next_action == "restart":
                break
            else:
                print("❌ Invalid choice. Returning to next action menu.")

if __name__ == "__main__":
    main()

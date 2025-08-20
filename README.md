# Data Extraction Tool

This is a Python-based Data Extraction Tool that allows users to extract text data from various sources, including PDF, DOCX, TXT, CSV, Excel files, and URLs. The program supports extracting words, sentences, or paragraphs and outputs structured results to terminal, CSV, or Excel with extended attributes and optional previews. A GUI version provides an interactive interface for users who prefer not to use the terminal.

---

## Table of Contents

1. Features
2. Folder Structure
3. Environment Setup
4. Dependencies
5. Usage (Terminal & GUI)
6. Navigation Commands
7. Notes
8. Example Usage

---

## Features

- Extract data from files or URLs
- Support for file types: `.pdf`, `.docx`, `.txt`, `.csv`, `.xls`, `.xlsx`
- Choose extraction type: word, sentence, paragraph
- Structured output with extended attributes:

  - Word Count
  - Character Length
  - Position (for words)
  - Sentence Index (for words)
  - Preview (optional)

- Save output with timestamped filenames to avoid overwriting
- Input folder (`input/`) for organized file management
- Output folder (`output/`) for saving results
- Flexible navigation:

  - `redo` → repeat current stage
  - `return` → go back one stage
  - `restart` → start over from source selection
  - `exit` → quit program

---

## Folder Structure

```
project_root/
│
├─ data_extractor.py        # Terminal version
├─ data_extractor_gui.py    # GUI version
├─ input/                   # Place files to be extracted here
├─ output/                  # Program saves results here
├─ README.md                # Documentation
└─ requirements.txt         # Python dependencies
```

> Note: The program will automatically create the `input/` and `output/` folders if they do not exist.

---

## Environment Setup

### 1. Install Python

- Recommended: Python 3.11
- Download: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### 2. Create and Activate a Virtual Environment

```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Windows Command Prompt
python -m venv venv
.\venv\Scripts\activate.bat

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Python Packages

The project includes a `requirements.txt` file with all necessary dependencies for both the terminal and GUI versions.

```bash
pip install -r requirements.txt
```

> This ensures that anyone cloning the repository can quickly set up the correct environment.

---

## Dependencies

- `pandas` → For handling CSV/Excel data
- `beautifulsoup4` → For parsing web pages
- `requests` → For fetching URL content
- `python-docx` → For reading DOCX files
- `pdfplumber` → For extracting PDF text
- `tabulate` → For displaying terminal tables
- `openpyxl` → For Excel file handling
- `lxml` → HTML/XML parsing
- `tkinter` → GUI interface (usually included with Python)

---

## Usage

### Terminal Version

1. Place files to extract in the `input/` folder (optional if using full paths).
2. Run the terminal program:

```bash
python data_extractor.py
```

3. Follow the prompts:

   - Choose source: file or URL
   - Select or enter file name/path
   - Choose extraction type: word, sentence, paragraph
   - Confirm selections
   - Select output method: terminal, CSV, Excel

**Output:** Files are saved in `output/` folder with timestamped filenames.

---

### GUI Version

1. Run the GUI program:

```bash
python data_extractor_gui.py
```

2. Follow the interactive prompts:

   - Choose source: File (from `input/` folder or browse) or URL
   - Select extraction type: word, sentence, paragraph
   - Preview results in a scrollable table with structured columns:

     - ID
     - Extracted Data
     - Type
     - Length
     - Preview (first 50 characters)

   - Save results automatically with timestamped filenames:

     - Example: `results_2025-08-20_14-32-15.xlsx`

   - Navigation options: `redo`, `return`, `restart`, `exit`

---

## Navigation Commands

| Command | Description                                 |
| ------- | ------------------------------------------- |
| exit    | Exit the program immediately                |
| redo    | Repeat the current stage without going back |
| return  | Go back to the previous stage               |
| restart | Go back to the "choose source" stage        |

---

## Notes

- Ensure the `input/` folder exists and contains files if using the folder search options.
- Outputs are saved in the `output/` folder with timestamped filenames to prevent overwriting.
- Invalid inputs will prompt re-entry or navigation commands.
- Structured output includes additional attributes for easier analysis and data processing.

---

## Example Usage

### Terminal Session

```
==== Data Extraction Tool ====
Choose source (file/url) or type 'exit'/'redo'/'restart': file

File selection options:
1. Enter full file path
2. Enter file name in 'input/' folder
3. Pick from list of files in 'input/' folder
Choose (1/2/3) or 'exit'/'redo'/'restart': 3
Available files in 'input/':
sample_docx.docx
sample_pdf.pdf
Choose a file number or 'exit'/'redo'/'restart': 1
Extract (word/sentence/paragraph) or 'exit'/'return'/'redo'/'restart': paragraph

✅ Current selections:
Source Type: file
File: sample_docx.docx
Extraction Type: paragraph

Confirm selections? (yes/no/exit/restart): yes

Output Options:
1. Display in terminal
2. Save to CSV
3. Save to Excel
Choose (1/2/3) or 'exit'/'return'/'redo'/'restart': 3
✅ Results saved to output/sample_docx_results_20250820_153245.xlsx

Next Actions:
1. Extract different data from the same file/url
2. Upload a new file/url
3. Exit
Choose (1/2/3) or 'restart': 3
👋 Exiting program. Goodbye!
```

### GUI Session

1. Click "Start Extraction"
2. Choose source type (File or URL)
3. Enter file name or browse from `input/` folder
4. Select extraction type
5. Preview the structured table in the pop-up window
6. Save results in CSV/Excel with auto timestamp
7. Use `redo`, `return`, `restart`, or `exit` for navigation

---

# Data Extraction Tool

This is a Python-based Data Extraction Tool that allows users to extract text data from various sources, 
including **PDF, DOCX, TXT, CSV, Excel files, and URLs**. The program supports extracting words, sentences, 
or paragraphs and outputs structured results to **terminal, CSV, or Excel** with extended attributes and optional previews.

---

## Table of Contents

- [Features](#features)
- [Folder Structure](#folder-structure)
- [Environment Setup](#environment-setup)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Navigation Commands](#navigation-commands)
- [Notes](#notes)

---

## Features

- Extract data from **files** or **URLs**
- Support for file types: `.pdf`, `.docx`, `.txt`, `.csv`, `.xls`, `.xlsx`
- Choose extraction type: `word`, `sentence`, `paragraph`
- Structured output with extended attributes:
  - Word Count
  - Character Length
  - Position (for words)
  - Sentence Index (for words)
  - Preview (optional)
- Save output with **timestamped filenames** to avoid overwriting
- Input folder (`input/`) for organized file management
- Output folder (`output/`) for saving results
- Flexible navigation:
  - `redo` → repeat current stage
  - `return` → go back one stage
  - `restart` → start over from source selection
  - `exit` → quit program

---

## Folder Structure
project_root/
│
├─ data_extractor.py # Main Python script
├─ input/ # Place files to be extracted here
├─ output/ # Program saves results here
├─ README.md # This documentation


> **Note:** The program will automatically create the `input/` and `output/` folders if they do not exist.

---

## Environment Setup

1. **Install Python**
   - Recommended: **Python 3.11**
   - Download: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Create a virtual environment**
   ```
   python -m venv venv

**Activate virtual environment:**

Windows (PowerShell):

```
.\venv\Scripts\Activate.ps1
```

Windows (Command Prompt):
```
.\venv\Scripts\activate.bat
```

Linux/macOS:
```
source venv/bin/activate
```

Install required Python packages
```
pip install pandas beautifulsoup4 requests python-docx pdfplumber tabulate openpyxl lxml
```

**Tip:** Always activate the virtual environment before running the program to ensure dependencies are loaded correctly.

# Dependencies

pandas → For handling CSV/Excel data

beautifulsoup4 → For parsing web pages

requests → For fetching URL content

python-docx → For reading DOCX files

pdfplumber → For extracting PDF text

tabulate → For displaying terminal tables

openpyxl → For Excel file handling

lxml → HTML/XML parsing

## Usage

Place files to extract in the input/ folder (optional if using full paths).

**Run the program:**
```
python data_extractor.py
```

**Follow the terminal prompts:**

Choose source: file or url

Select or enter file name/path

Choose extraction type: word, sentence, paragraph

Confirm selections

Select output method: terminal, CSV, Excel

Output files will be saved in the output/ folder with a timestamped filename.

## Navigation Commands

During prompts, you can use the following commands:

**Command	Description**
exit	    Exit the program immediately
redo	    Repeat the current stage without going back
return	  Go back to the previous stage
restart	  Go back to the "choose source" stage
Notes

## Ensure the input/ folder exists and contains files if using the folder search options.

Outputs are saved in output/ folder with timestamped filenames to prevent overwriting.

Invalid inputs will prompt re-entry or navigation commands.

Structured output includes additional attributes for easier analysis and data processing.

## Example Usage

### Terminal Session


==== Data Extraction Tool ====
Choose source (file/url) or type 'exit'/'redo'/'restart': file

File selection options:
1. Enter full file path
2. Enter file name in 'input/' folder
3. Pick from list of files in 'input/' folder
Choose (1/2/3) or 'exit'/'redo'/'restart': 3

Available files in 'input/':
1. sample_docx.docx
2. sample_pdf.pdf
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



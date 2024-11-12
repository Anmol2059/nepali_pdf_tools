# Nepali PDF Tools

An interactive tool for processing Nepali PDF files, built with Streamlit, Tesseract OCR, and other PDF manipulation libraries.

## Features
- Removes images from PDFs.
- Converts PDF pages to images.
- Extracts text with OCR and creates a Nepali corpus.
- Deletes intermediate images after processing.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Anmol2059/nepali_pdf_tools.git
cd nepali_pdf_tools
```

### 2. Make run.sh executable and run
```bash
chmod +x run.sh
./run.sh
```

This script will:

Create a Conda environment, install dependencies, and start the Streamlit app.
Usage
Open Streamlit in your browser as prompted.
Upload a PDF file.
The app processes the PDF, generates a Nepali text corpus, and deletes intermediate images.
Directory Structure
Output/: Contains subdirectories for each processed PDF.

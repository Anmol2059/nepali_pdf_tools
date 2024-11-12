#!/bin/bash

echo "Creating a new Conda environment named 'pdf_processing_env'..."
conda create -n pdf_processing_env python=3.9 -y

echo "Activating the environment..."
source activate pdf_processing_env

echo "Installing required packages..."
pip install streamlit pytesseract pdf2image pillow pymupdf tqdm

echo "Setting up pdf2image dependencies..."
if conda install -c conda-forge poppler -y; then
    echo "Poppler installed successfully via Conda."
elif command -v sudo &> /dev/null; then
    echo "Conda installation of Poppler failed. Trying with sudo apt-get..."
    sudo apt-get update && sudo apt-get install -y poppler-utils && echo "Poppler installed successfully via apt-get."
else
    echo "Poppler installation skipped. Neither Conda nor sudo apt-get were successful."
fi

echo "Starting Streamlit app..."
streamlit run app.py

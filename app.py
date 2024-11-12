import streamlit as st
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import fitz
import re
import os
import shutil  # For deleting the directory at the end

# Directory for output files
output_base_dir = "Output"
if not os.path.exists(output_base_dir):
    os.makedirs(output_base_dir)

def remove_images(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)
    for page in doc:
        img_list = page.get_images()
        for img in img_list:
            page.delete_image(img[0])
    doc.save(output_pdf)

def make_nepali_corpus(extracted_string, output_path):
    filtered_text = extracted_string.replace("|", '।')
    nepali_digits = '[\u0966-\u096F]'
    pattern = f'({nepali_digits})।({nepali_digits})'
    replaced_text = re.sub(pattern, r'\1/\2', filtered_text)
    sections = replaced_text.split('\n\n')
    sentence_complete_flag = False
    try:
        if sections[-1][-2] == '।':
            sentence_complete_flag = True
    except:
        sentence_complete_flag = False

    linebreak_removal = [element.replace("\n", ' ') for element in sections]
    final_list = [re.split('[।?]', element) for element in linebreak_removal]
    final_list = [item.strip() for sublist in final_list for item in sublist if item.strip()]

    if sentence_complete_flag == False:
        last_line = final_list[-1]
        final_list = final_list[:-1]
    
    with open(output_path, 'a') as output_list:
        for i, element in enumerate(final_list):
            if len(element) < 7:
                continue
            if i != (len(final_list) - 1) and final_list[i + 1][0] == '(':
                output_list.write(f"{element} ")
                continue
            output_list.write(f"{element} ।\n")
        if sentence_complete_flag == False:
            output_list.write(f"{last_line} ")

st.title("Nepali Corpus Maker")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    # Set up directories
    pdf_name = os.path.splitext(uploaded_file.name)[0]
    file_output_dir = os.path.join(output_base_dir, pdf_name)
    images_dir = os.path.join(file_output_dir, f"{pdf_name}_images")
    if not os.path.exists(file_output_dir):
        os.makedirs(file_output_dir)
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    # Save the uploaded PDF file
    uploaded_pdf_path = os.path.join(file_output_dir, f"{pdf_name}_uploaded.pdf")
    with open(uploaded_pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # 1. Remove images from PDF
    image_removed_path = os.path.join(file_output_dir, f"{pdf_name}_imageremoved.pdf")
    st.write("Removing images from PDF...")
    remove_images(uploaded_pdf_path, image_removed_path)
    st.write("Images removed successfully.")

    # 2. Convert PDF to images
    st.write("Converting PDF to images...")
    pages = convert_from_path(image_removed_path)
    total_pages = len(pages)
    st.write(f"Total pages: {total_pages}")

    # 3. Define intervals (segmenting in batches of 10 pages each)
    intervals = [list(range(i, min(i + 10, total_pages))) for i in range(0, total_pages, 10)]

    # 4. Process each interval with a progress bar
    st.write("Processing pages...")
    progress_bar = st.progress(0)
    corpus_output_path = os.path.join(file_output_dir, f"{pdf_name}_corpus.txt")
    
    # Track total pages processed
    processed_pages = 0
    status_text = st.empty()

    for idx, interval in enumerate(intervals):
        for page_num in interval:
            processed_pages += 1
            # Update the status in the same placeholder
            status_text.text(f"Processing pages: {processed_pages}/{total_pages}")

            # Save page image
            page = pages[page_num]
            img_path = os.path.join(images_dir, f"page_{page_num + 1}.png")
            page.save(img_path)

            # Extract text from image
            extracted_string = pytesseract.image_to_string(page, lang='nep+eng')

            # Create Nepali corpus
            make_nepali_corpus(extracted_string, corpus_output_path)
        
        # Update progress bar after each interval
        progress_bar.progress(processed_pages / total_pages)
    
    st.write(f"Processing complete. Nepali corpus saved at `{corpus_output_path}`.")

    # Delete all images after processing
    if os.path.exists(images_dir):
        shutil.rmtree(images_dir)
        st.write(f"All intermediate images deleted from `{images_dir}`.")
else:
    st.write("Please upload a PDF file to start the process.")

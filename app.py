import streamlit as st
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import os

# Directory for output files
output_base_dir = "Output"
if not os.path.exists(output_base_dir):
    os.makedirs(output_base_dir)

def save_verified_text(text, page_num, output_path):
    """Save verified text with page number marker"""
    text = text.replace("|", '।')  # Replace '|' with the Nepali danda (।)
    with open(output_path, 'a', encoding="utf-8") as output_file:
        output_file.write(f"[Page {page_num + 1}]\n{text}\n\n")

st.title("Nepali Corpus Maker - Manual Review for Scanned PDFs")

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

    # Convert PDF to images
    st.write("Converting PDF to images...")
    pages = convert_from_path(uploaded_pdf_path)
    total_pages = len(pages)
    st.write(f"Total pages: {total_pages}")

    # Save images and prepare for display
    page_images = []
    for page_num, page in enumerate(pages):
        img_path = os.path.join(images_dir, f"page_{page_num + 1}.png")
        page.save(img_path)
        page_images.append(img_path)

    # Initialize session state for page tracking
    if "current_page" not in st.session_state:
        st.session_state.current_page = 0
    if "verified_pages" not in st.session_state:
        st.session_state.verified_pages = set()

    current_page = st.session_state.current_page

    # Only proceed if we haven't finished all pages
    if current_page < total_pages:
        current_image = page_images[current_page]
        
        # Display page number and progress
        st.write(f"Currently editing page {current_page + 1} of {total_pages}")
        st.progress((len(st.session_state.verified_pages)) / total_pages)

        # Layout for side-by-side display
        col1, col2 = st.columns([3, 2])

        # Display page image on the left
        with col1:
            st.image(current_image, caption=f"Page {current_page + 1}", use_container_width=True)

        # Perform OCR and show editable text on the right
        with col2:
            # Only perform OCR if we haven't stored the text yet
            if f"ocr_text_{current_page}" not in st.session_state:
                extracted_text = pytesseract.image_to_string(Image.open(current_image), lang='nep+eng')
                st.session_state[f"ocr_text_{current_page}"] = extracted_text

            # Editable text area
            edited_text = st.text_area(
                "Edit OCR Text",
                value=st.session_state[f"ocr_text_{current_page}"],
                height=500,
                key=f"text_area_{current_page}"
            )
            
            # Save and continue button
            corpus_output_path = os.path.join(file_output_dir, f"{pdf_name}_corpus.txt")
            if st.button("Verify, Save and Continue to Next Page"):
                save_verified_text(edited_text, current_page, corpus_output_path)
                st.session_state.verified_pages.add(current_page)
                st.session_state.current_page += 1
                st.rerun()

        # Show verification progress
        verified_count = len(st.session_state.verified_pages)
        st.write(f"Progress: {verified_count}/{total_pages} pages verified")

    # Show completion message when all pages are done
    else:
        st.success(f"🎉 All {total_pages} pages have been verified and saved!")
        st.write(f"Complete corpus saved at: {os.path.join(file_output_dir, f'{pdf_name}_corpus.txt')}")
        
        # Option to start over
        if st.button("Start Over"):
            st.session_state.current_page = 0
            st.session_state.verified_pages = set()
            st.rerun()

else:
    st.write("Please upload a PDF file to start the process.")
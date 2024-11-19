import streamlit as st
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import os

# Directory for output files
output_base_dir = "Output"
if not os.path.exists(output_base_dir):
    os.makedirs(output_base_dir)

def make_nepali_corpus(text, output_path):
    text = text.replace("|", '।')  # Replace '|' with the Nepali danda (।)
    with open(output_path, 'a', encoding="utf-8") as output_file:
        output_file.write(text + "\n")

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

    # Initialize session state for page navigation and text storage
    if "current_page" not in st.session_state:
        st.session_state.current_page = 0
    if "page_texts" not in st.session_state:
        st.session_state.page_texts = [""] * total_pages  # Store texts for all pages

    # Get the current page
    current_page = st.session_state.current_page
    current_image = page_images[current_page]

    # Perform OCR on the current page if text is not already edited
    if not st.session_state.page_texts[current_page]:
        extracted_text = pytesseract.image_to_string(Image.open(current_image), lang='nep+eng')
        st.session_state.page_texts[current_page] = extracted_text

    # Layout for side-by-side display
    col1, col2 = st.columns([3, 2])  # More space to the image (3:2 ratio)

    # Display page image on the left
    with col1:
        st.image(current_image, caption=f"Page {current_page + 1}", use_container_width=True)

    # Editable text area on the right
    with col2:
        st.text_area(
            "Edit OCR Text",
            value=st.session_state.page_texts[current_page],
            height=500,
            key="text_area",
            on_change=lambda: st.session_state.page_texts.__setitem__(current_page, st.session_state.text_area),
        )

    # Save current page's text automatically when navigating
    corpus_output_path = os.path.join(file_output_dir, f"{pdf_name}_corpus.txt")

    # Navigation buttons
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("Previous Page") and current_page > 0:
            # Save the current page's text
            make_nepali_corpus(st.session_state.page_texts[current_page], corpus_output_path)
            # Move to the previous page
            st.session_state.current_page -= 1
    with col_nav2:
        if st.button("Next Page") and current_page < total_pages - 1:
            # Save the current page's text
            make_nepali_corpus(st.session_state.page_texts[current_page], corpus_output_path)
            # Move to the next page
            st.session_state.current_page += 1

    # Display completion message
    if current_page == total_pages - 1:
        st.write(f"Corpus generation complete. File saved at `{corpus_output_path}`.")
else:
    st.write("Please upload a PDF file to start the process.")

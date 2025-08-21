
import streamlit as st
import pdfplumber
import re
import os
from collections import defaultdict
from PyPDF2 import PdfMerger

# -------------------------------
# Helper Functions
# -------------------------------

def extract_text(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_postcode(text):
    """Extract UK postcode from text."""
    postcode_pattern = r'\b([A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2})\b'
    match = re.search(postcode_pattern, text)
    if match:
        return match.group(0).replace(" ", "")
    return None

def merge_pdfs(pdf_list, output_path):
    """Merge multiple PDFs into one."""
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()

# -------------------------------
# Streamlit App
# -------------------------------

st.title("📄 Invoice Grouping by UK Postcode")

st.write("Upload multiple PDF invoices and get merged PDFs grouped by UK postal codes.")

uploaded_files = st.file_uploader(
    "Upload PDF invoices", accept_multiple_files=True, type="pdf"
)

if uploaded_files:
    # Create temp folder for uploaded PDFs
    temp_folder = "temp_invoices"
    os.makedirs(temp_folder, exist_ok=True)

    # Save uploaded PDFs
    for uploaded_file in uploaded_files:
        with open(os.path.join(temp_folder, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
    
    st.success(f"{len(uploaded_files)} invoices uploaded successfully!")

    if st.button("Generate Grouped PDFs"):
        grouped_invoices = defaultdict(list)
        output_folder = "grouped_invoices"
        os.makedirs(output_folder, exist_ok=True)

        # Process each PDF
        for pdf_file in os.listdir(temp_folder):
            pdf_path = os.path.join(temp_folder, pdf_file)
            text = extract_text(pdf_path)
            postcode = extract_postcode(text)
            if postcode:
                grouped_invoices[postcode].append(pdf_path)

        # Merge PDFs per postcode
        download_links = []
        for postcode, pdf_list in grouped_invoices.items():
            output_path = os.path.join(output_folder, f"{postcode}.pdf")
            merge_pdfs(pdf_list, output_path)
            download_links.append(output_path)
        
        if download_links:
            st.success("Grouped PDFs created successfully!")
            st.write("Download your grouped PDFs below:")
            for file in download_links:
                with open(file, "rb") as f:
                    st.download_button(
                        label=f"Download {os.path.basename(file)}",
                        data=f,
                        file_name=os.path.basename(file),
                        mime="application/pdf"
                    )
        else:
            st.warning("No UK postcodes found in uploaded invoices.")
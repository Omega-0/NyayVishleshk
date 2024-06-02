import camelot
import os
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

def extract_text_with_delimiters(pdf_path):
    # Extract text using PDFMiner
    laparams = LAParams()
    text = extract_text(pdf_path, laparams=laparams)
    pages = text.split('\x0c')  # Split text by pages using form feed character
    
    extracted_text = ""
    for i, page_text in enumerate(pages):
        print(f"Processing page {i+1}")
        if page_text.strip():
            delimiter = f"page_number_{i + 1}\n"
            extracted_text += f"{delimiter}{page_text.strip()}\n{delimiter}\n"
    
    return extracted_text

def extract_tables(pdf_path):
    # Extract tables using Camelot
    tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')
    tables_json = []
    for table in tables:
        tables_json.append(table.df.to_json(orient='split'))
    return tables_json

def process_pdf(pdf_path):
    # Extract text with delimiters
    text_with_delimiters = extract_text_with_delimiters(pdf_path)

    # Extract tables
    tables_json = extract_tables(pdf_path)
    
    return text_with_delimiters, tables_json

def save_results(text, tables_json, output_path):
    # Save extracted text and tables in a single file
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(text)
        if tables_json:
            output_file.write("\n--- Begin Tables ---\n")
            for i, table_json in enumerate(tables_json):
                output_file.write(f"Table {i + 1}:\n")
                output_file.write(table_json)
                output_file.write("\n")

def extract_text(pdf_path,output_directory = "saved_logs"):
    # Paths to your PDF file and output file
    file_name = pdf_path.split('\\')[-1][:-4]
    os.makedirs(output_directory,exist_ok=True)
    output_txt_path = os.path.join(output_directory,file_name+'.txt')

    # Process the PDF
    text_with_delimiters, tables_json = process_pdf(pdf_path)

    # Save the results
    save_results(text_with_delimiters, tables_json, output_txt_path)

    print("Text and tables extracted successfully!")

extract_text('referrence_docs\IPC.pdf')
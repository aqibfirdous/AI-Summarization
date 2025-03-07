import PyPDF2

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF document.

    Parameters:
      file_path (str): Path to the PDF file.

    Returns:
      str: Extracted text.
    """
    text = ""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    return text

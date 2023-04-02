import pdfplumber
from typing import Union
from pathlib import Path


def extract_text_from_pdf(pdf_path: Union[str, Path]) -> str:
    """
    Extract text from the given PDF file.

    :param pdf_path: The path to the input PDF file.
    :type pdf_path: Union[str, Path]
    :return: The extracted text from the PDF.
    :rtype: str
    """
    pdf_path = Path(pdf_path)
    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text()

    return extracted_text

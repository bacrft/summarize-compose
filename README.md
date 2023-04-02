# PDF Text Extractor and Summarizer

This project extracts text from PDF files and summarizes the extracted text using the OpenAI Completion API. The user can choose the number of recursive loops to summarize the text further.

## Requirements

- Python 3.7 or higher
- `pdfplumber` library for PDF text extraction
- `openai` library for interacting with the OpenAI Completion API

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/samimhidia1/pdf_text_extractor_and_summarizer.git
    ```
   
2. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```
3. Set your OpenAI API key as an environment variable or directly in the `main.py` file.

## Usage

1. Place your input PDF files in the `input_pdfs` folder.

2. Modify the `main.py` script to include the desired input PDF file and the number of recursive loops for summarization.

3. Run the `main.py` script:

    ```bash
    python main.py
    ```

4. Check the `output/extracted_texts` folder for the extracted text files and the `output/summarized_texts` folder for the summarized text files.

## Customization

- Modify the `APIRequestConfig` in the `main.py` file to change the prompt or other API parameters.
- Modify the `SummarizationConfig` in the `main.py` file to change the chunk size for text summarization.


# PDF Text Extractor and Summarizer

This project extracts text from PDF files and summarizes the extracted text using the OpenAI Completion API. The user can choose the number of recursive loops to summarize the text further.

## Requirements

- Python 3.10 or higher
- `pdfplumber` library for PDF text extraction
- `openai` library for interacting with the OpenAI Completion API

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/samimhidia1/summarize-compose.git
    ```
   
2. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```
3. Set your OpenAI API key as an environment variable or directly in the `openai_apikey.txt` file.

## Usage

1. run the `main.py` file:

    ```bash
    python main.py
    ```

2. Enter the name of an existing project or create a new one by entering a new name.

3. Add the PDF files to the project input folder.

4. Choose summarize by pressing 's' and Enter.

5. Once the summarization is complete, the summarized text will be saved in the project output folder.

6. Rerun the main.py file to compose an essay from the summarized text.

7. Enter the name of the summarized project which you want to compose an essay from.

8. Choose compose by pressing 'c' and Enter.

9. Enter the question of the essay.

10. Enter the instructions of the essay.

## Customization

- Modify the `APIRequestConfig` in the `main.py` file to change the prompt or other API parameters.
- Modify the `SummarizationConfig` in the `main.py` file to change the chunk size for text summarization.
- Modify the chunk size in the `main` file to change the chunk size for text summarization.
- Modify the size_reduction_factor in the `main` file to change the size reduction factor for text summarization.
- Modify the `EssayCompositionConfig` in the `main.py` file to change the prompt or other API parameters.
- Modify the content in the main.py at line 156 to change the prompt for essay composition.

## TODO

- [ ] Add support for other file formats.
- [ ] Add support for other summarization and composition APIs.
- [ ] Add support for other summarization and composition models.
- [ ] Add other summarization and composition prompts.
- [ ] Add semantic search to find the most relevant text from summarized text to choose as the prompt for essay composition without going over the API character limit.
- [ ] Add support for other languages.
- [ ] Add support for pinecone search.
- [ ] Add support for langchain to ask questions in natural language through a set of documents
- [ ] Add prompt engineering techniques to improve the quality of the essay composition.
- [ ] Add support for Hugging Face API transformers to avoid paying for the OpenAI API.
- [ ] Make a better Documentation.
- 
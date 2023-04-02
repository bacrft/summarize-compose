import os
import time
from typing import Union, Optional
from pathlib import Path
from dataclasses import dataclass
from pdf_extraction import extract_text_from_pdf
from text_summarization import summarize_text, SummarizationConfig
from api_interaction import APICompletionRequestConfig, APIChatRequestConfig, call_openai_api_chat
from chat_history_construction import ComposeConfiguration, split_text_into_chunks, build_history_file


@dataclass
class UserInputConfig:
    """User Input Configuration

    A dataclass to store the configuration for the user input.
    """
    project_name: str
    pdf_files: Optional[list[Union[str, Path]]] = None

    def __post_init__(self):
        self.project_path = "projects/" + self.project_name
        self.pdf_files = [self.project_path + "/input/" + str(pdf_file)
                          for pdf_file in os.listdir(self.project_path + "/input")
                          if pdf_file.endswith(".pdf")]


@dataclass
class UserInputConfigCompose:
    """User Input Configuration

    A dataclass to store the configuration for the user input.
    """
    project_name: str
    question: str
    instructions: str
    summarized_texts: Optional[list[Union[str, Path]]] = None

    def __post_init__(self):
        self.project_path = "projects/" + self.project_name + "/output/summarized_texts"
        self.summarized_texts = [self.project_path + "/" + str(summarized_text) for summarized_text
                                 in os.listdir(self.project_path)]


def save_text_to_file(text: str, file_path: Union[str, Path]) -> None:
    """
    Save the input text to the specified file path.

    :param text: The input text to be saved.
    :type text: str
    :param file_path: The file path where the text will be saved.
    :type file_path: Union[str, Path]
    """
    with open(file_path, "w") as output_file:
        output_file.write(text)


def open_file(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def summarize_documents(project_name: str):
    """
    Summarize the documents in the input folder of the project.

    :param project_name: The name of the project.
    :type project_name: str

    """
    openai_apikey = open("openai_apikey.txt", "r").read()

    # Get the user input configuration
    userInput = UserInputConfig(
        project_name=project_name,
    )

    # Choice of prompt
    summarize_prompt = open_file("prompts/summarize_prompt.txt")
    summarize_prompt_2 = open_file("prompts/summarize_prompt_2.txt")
    summarize_bullets_prompt = open_file("prompts/summarize_bullets_prompt.txt")
    summarize_bullets_prompt_fr = open_file("prompts/summarize_bullets_prompt_fr.txt")

    # Define the OpenAI API request configuration
    api_request_config = APICompletionRequestConfig(
        api_key=openai_apikey,
        prompt=summarize_bullets_prompt_fr
    )

    # Define the summarization configuration
    summarizationConfig = SummarizationConfig(
        chunk_size=256,
        api_request_config=api_request_config,
        project_name=userInput.project_name
    )

    for pdf_file in userInput.pdf_files:
        time_str = time.strftime("%Y%m%d-%H%M%S")
        pdf_file_name = Path(pdf_file).stem
        print(f"Processing file: {pdf_file_name}")
        print(f"Extracting and summarizing from file...")
        extracted_text = extract_text_from_pdf(pdf_file)
        save_text_to_file(extracted_text,
                          f"projects/{userInput.project_name}/output/extracted_texts"
                          f"/{pdf_file_name}_{time_str}.txt")

        summarized_text = summarize_text(extracted_text, summarizationConfig, pdf_file_name)
        save_text_to_file(summarized_text,
                          f"projects/{userInput.project_name}/output/summarized_texts"
                          f"/{pdf_file_name}_summary_{time_str}.txt")
        print(f"Finished processing file: {pdf_file_name}")


def compose_essay(project_name, question, instructions):
    """
    Compose the essay from the summarized texts.

    :param project_name: The name of the project.
    :type project_name: str
    :param question: The question to be answered in the essay.
    :type question: str
    :param instructions: The instructions for the essay.
    :type instructions: str

    """
    openai_apikey = open("openai_apikey.txt", "r").read()

    # Get the user input configuration
    userInput = UserInputConfigCompose(
        project_name=project_name,
        question=question,
        instructions=instructions
    )

    # Choice of prompt
    compose_prompt = open_file("prompts/compose_prompt.txt").replace("<<<QUESTION>>>", question) \
        .replace("<<<INSTRUCTIONS>>>", instructions)
    compose_prompt_fr = open_file("prompts/compose_prompt_fr.txt").replace("<<<QUESTION>>>", question) \
        .replace("<<<INSTRUCTIONS>>>", instructions)

    # loop through the summarized texts and add them to a single string
    summarized_texts = ""

    for summarized_text in userInput.summarized_texts:
        summarized_texts += open_file(summarized_text) + " "

    split_summarized_texts = split_text_into_chunks(summarized_texts, 256)

    history_file = build_history_file(userInput.project_name, split_summarized_texts)

    print(history_file)

    history_file.append({'role': 'user', 'content': compose_prompt_fr})

    # Define the composition configuration
    API_Chat_Request_Config = APIChatRequestConfig(api_key=openai_apikey, messages=history_file)

    compositionConfig = ComposeConfiguration(
        project_name=userInput.project_name,
        chunk_size=300,
        api_request_config=API_Chat_Request_Config
    )

    # Compose the essay
    essay = call_openai_api_chat(API_Chat_Request_Config)

    # Save the essay to a file
    save_text_to_file(essay, f"projects/{userInput.project_name}/compose/essay.txt")


if __name__ == "__main__":

    openai_apikey = open("openai_apikey.txt", "r").read()

    print("Welcome to the PDF text extraction and summarization tool!")
    project_name = str(input("Enter the name of the project: "))
    if not os.path.exists("projects/" + project_name):
        print("The project does not exist. Do you want to create it? (y/n)")
        create_project = str(input())
        if create_project == "y":
            # create a folder inside the projects folder with the name given by the user
            os.makedirs("projects/" + project_name, exist_ok=True)
            os.makedirs("projects/" + project_name + "/input", exist_ok=True)
            os.makedirs("projects/" + project_name + "/output", exist_ok=True)
            os.makedirs("projects/" + project_name + "/output/extracted_texts", exist_ok=True)
            os.makedirs("projects/" + project_name + "/output/summarized_texts", exist_ok=True)
            os.makedirs("projects/" + project_name + "/output/chunks", exist_ok=True)
            os.makedirs("projects/" + project_name + "/compose", exist_ok=True)
            print("Project created successfully!")
            print("Please add the PDF files to the input folder and run the program again.")
            exit()
        else:
            exit()
    else:
        if not os.path.exists("projects/" + project_name + "/input"):
            os.makedirs("projects/" + project_name + "/input", exist_ok=True)
        if not os.path.exists("projects/" + project_name + "/output"):
            os.makedirs("projects/" + project_name + "/output", exist_ok=True)
        if not os.path.exists("projects/" + project_name + "/output/extracted_texts"):
            os.makedirs("projects/" + project_name + "/output/extracted_texts", exist_ok=True)
        if not os.path.exists("projects/" + project_name + "/output/summarized_texts"):
            os.makedirs("projects/" + project_name + "/output/summarized_texts", exist_ok=True)
        if not os.path.exists("projects/" + project_name + "/output/chunks"):
            os.makedirs("projects/" + project_name + "/output/chunks", exist_ok=True)
        if not os.path.exists("projects/" + project_name + "/compose"):
            os.makedirs("projects/" + project_name + "/compose", exist_ok=True)

    # ask the user if he wants to compose the essay or summarize the pdf files
    print("Do you want to compose an essay or summarize the pdf files? (c/s)")
    user_input = str(input())
    if user_input == "c":
        # ask the user for the question of the essay
        print("Enter the question of the essay:")
        question = str(input("question:"))
        # ask the user for the instructions of the essay
        print("Do you have some instructions regarding the writing the essay (number of words, structure to follow, "
              "etc.)? If yes, enter them here. If not, just press enter")
        instructions = str(input("instructions:"))
        compose_essay(project_name, question, instructions)
    elif user_input == "s":
        summarize_documents(project_name)

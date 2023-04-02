import json
from dataclasses import dataclass
from typing import List

from api_interaction import APICompletionRequestConfig, APIChatRequestConfig


@dataclass
class ComposeConfiguration:
    """
    A dataclass to store the configuration for the text summarization process.
    """
    project_name: str
    api_request_config: APIChatRequestConfig
    chunk_size: int = 300


def split_text_into_chunks(text: str, chunk_size: int) -> List[str]:
    """
    Split the input text into chunks of the specified size.

    :param text: The input text to be split.
    :type text: str
    :param chunk_size: The desired size of the text chunks.
    :type chunk_size: int
    :return: A list of text chunks.
    :rtype: List[str]
    """
    words = text.split()
    chunks = [
        " ".join(words[i: i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]
    return chunks


def save_history_file(project_name: str, history_file: json) -> None:
    """
    Save the history file to disk.

    :param project_name: The name of the project.
    :type project_name: str
    :param history_file: The history file.
    :type history_file: json

    """
    path = "projects/{}/history_file.json".format(project_name)
    with open(path, "w") as f:
        json.dump(history_file, f)


def build_history_file(project_name: str, summarized_texts: List[str]) -> json:
    """
    Build the history file for chatGPT.

    :param project_name: The name of the project.
    :type project_name: str
    :param summarized_texts: The list of summarized texts.
    :type summarized_texts: List[str]
    :return: The history file.
    :rtype: json
    """
    history_file = list()
    history_file.append(
        {
            "role": "system",
            "content": "Act as an essay writer and compose an essay based on the provided documents and instructions. "
                       "Analyze the documents to come up with a concise and compelling thesis statement, "
                       "draw relevant conclusions from the evidence presented, and support your claims with reliable "
                       "sources. Pay close attention to the structure of the essay, ensuring that each section "
                       "contains only relevant information and logically transitions from one point to the next. "
                       "Lastly, review everything for accuracy and make sure that all arguments are properly "
                       "supported by evidence. Make sure to follow the provided instructions closely when crafting "
                       "your essay. I will tell you when to start writing by saying WRITE THE ESSAY."
        }
    )
    for i, text in enumerate(summarized_texts):
        history_file.append(
            {
                "role": "user",
                "content": text
            }
        )
        history_file.append(
            {
                "role": "assistant",
                "content": "Ok, I have understood this part. I am waiting for your signal to start writing."
            }
        )

    save_history_file(project_name=project_name, history_file=history_file)

    return history_file

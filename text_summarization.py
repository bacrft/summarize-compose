import math
import time
from typing import List
from dataclasses import dataclass
from api_interaction import call_openai_api, APICompletionRequestConfig


@dataclass
class SummarizationConfig:
    """Summarization Configuration

    A dataclass to store the configuration for the text summarization process.
    """
    project_name: str
    chunk_size: int = 300
    api_request_config: APICompletionRequestConfig = APICompletionRequestConfig(api_key="")


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


def summarize_text(text: str, config: SummarizationConfig, pdf_file_name: str) -> str:
    """
    Summarize the input text using the given summarization configuration.

    :param pdf_file_name:
    :param text: The input text to be summarized.
    :type text: str
    :param config: The summarization configuration.
    :type config: SummarizationConfig
    :return: The summarized text.
    :rtype: str
    """
    chunks = split_text_into_chunks(text, config.chunk_size)
    summarized_chunks = list()

    print("length of text to summarize: {}".format(len(text)))
    # reduce the text to one-quarter of its original size
    size_reduction_factor = 0.20
    size_summarized_text = len(text)
    threshold = len(text) * size_reduction_factor
    i = 0
    while size_summarized_text > threshold:
        summarized_chunks = list()
        # loop through the chunks and create a list of modulo 20 chunks
        for rounds in range(0, len(chunks), 20):
            print("processing batch: {} of {}".format(int(rounds / 20 + 1), len(chunks) // 20 + 1))
            # create a list of chunks to be summarized in parallel
            chunks_to_summarize = chunks[rounds: rounds + 20]
            summarized_chunks += call_openai_api(chunks=chunks_to_summarize,
                                                 config=config.api_request_config)
        chunks = summarized_chunks
        chunks = split_text_into_chunks(" ".join(chunks), config.chunk_size)
        summarized_text = " ".join(summarized_chunks)
        size_summarized_text = len(summarized_text)
        print("Summarized text length: {}".format(size_summarized_text))
        # save the summarized text to a file for debugging purposes
        chunk_path = "projects/" + config.project_name + "/output/chunks/"
        time_str = time.strftime("%Y%m%d-%H%M%S")
        with open(chunk_path + "{}_".format(time_str) + pdf_file_name + "_chunk_{}.txt".format(i), "w") as output_file:
            output_file.write(summarized_text)
        i += 1
        print("recursive loop: {}".format(i))

    summarized_text = " ".join(summarized_chunks)

    final_reduction_factor = 1/(len(text) / size_summarized_text)

    print("Real Reduction factor: {}".format(final_reduction_factor))

    return summarized_text

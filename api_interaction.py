import openai
from typing import Optional
from dataclasses import dataclass


@dataclass
class APICompletionRequestConfig:
    """API Request Configuration

    A dataclass to store the configuration for an OpenAI API request.
    """
    api_key: str
    model: str = "text-curie-001"
    prompt: str = ""
    temperature: float = 0.4
    max_tokens: int = 667
    frequency_penalty: float = 0.9
    presence_penalty: float = 0.6
    n: int = 1
    stop: Optional[str] = None


@dataclass
class APIChatRequestConfig:
    """API Request Configuration

    A dataclass to store the configuration for an OpenAI API request.
    """
    api_key: str
    messages: list[dict[str, str]]
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    top_p: float = 1.0
    frequency_penalty: float = 0.7
    presence_penalty: float = 0.0
    n: int = 1
    stop: Optional[str] = None


def call_openai_api(chunks: list[str],
                    config: APICompletionRequestConfig) -> list[str]:
    """
    Call the OpenAI API to summarize the given text chunk.

    :param chunks: The list of text chunks.
    :type chunks: list[str]
    :param config: The API request configuration.
    :type config: APIRequestConfig
    :return: The summarized text chunk.
    :rtype: str
    """
    openai.api_key = config.api_key

    prompts = [config.prompt.format(chunk=chunk) for chunk in chunks]

    response = openai.Completion.create(
        engine=config.model,
        prompt=prompts,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        frequency_penalty=config.frequency_penalty,
        presence_penalty=config.presence_penalty,
        n=config.n,
        stop=config.stop,
    )

    summarized_chunks = list()

    for summary in response.choices:
        summarized_chunks.append(summary.text.strip())

    return summarized_chunks


def call_openai_api_chat(config: APIChatRequestConfig) -> str:
    """
    Call the OpenAI API to summarize the given text chunk.

    :param config: The API request configuration.
    :type config: APIRequestConfig
    :return: The summarized text chunk.
    :rtype: str
    """
    openai.api_key = config.api_key

    response = openai.ChatCompletion.create(
        model=config.model,
        messages=config.messages,
        temperature=config.temperature,
        top_p=config.top_p,
        frequency_penalty=config.frequency_penalty,
        presence_penalty=config.presence_penalty,
        n=config.n,
        stop=config.stop
    )

    message = response.choices[0].message.content.strip()

    return message

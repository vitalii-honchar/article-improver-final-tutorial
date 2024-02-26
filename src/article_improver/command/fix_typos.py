from article_improver.chat_gpt.chat_gpt import ChatGpt, MODEL_GPT_3, MAX_TOKENS
from article_improver.chat_gpt.compressor import compress_with_saving_punctuation
from article_improver import pdf, output
import json
import re

FIELD_TEXT = "text"

PROMPT = f"""
As an SEO optimization assistant, your task is to evaluate an article provided within triple quotes. Analyze typos in the text and provide fix for the typos:

1. Fixed text without explanation of mistakes.

Please format your response as a JSON object with the following fields:
- "{FIELD_TEXT}": A fixed text in the format of string array where each element is separate sentence. Example: ["The fixed sentence 1.", "The fixed sentence 2!"]
Ensure the response excludes extraneous formatting or labels, presenting only the JSON object for direct usability in Python.
"""

REGEX_SPLIT_TO_SENTENCES = r"(?<=\w)[.!?;:](?=\s|$)"


def convert_to_sentences(content: str) -> list[str]:
    sentences = re.split(REGEX_SPLIT_TO_SENTENCES, content)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def create_batches(content: str, model: str) -> list[str]:
    sentences = convert_to_sentences(content)
    if len(sentences) == 0:
        return []

    max_tokens = MAX_TOKENS[model]
    batches = []

    while len(sentences) > 0:
        next_sentence = sentences.pop()
        if len(batches) == 0 or len(batches[-1] + next_sentence) >= max_tokens:
            batches.append(next_sentence)
        else:
            batches[-1] += next_sentence

    return batches


async def handle(chat_gpt: ChatGpt, filename: str):
    content = compress_with_saving_punctuation(pdf.read_pdf(filename))
    batches = create_batches(content, MODEL_GPT_3)

    for batch in batches:
        completion = await chat_gpt.get_completion(PROMPT, batch, MODEL_GPT_3)
        completion_json = json.loads(completion)
        output.print_list_field(":smiley: Fixed typos", FIELD_TEXT, completion_json)

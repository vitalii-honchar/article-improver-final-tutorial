from loguru import logger
from article_improver.chat_gpt.chat_gpt import ChatGpt, MODEL_GPT_4
from article_improver.chat_gpt.compressor import compress
from article_improver import pdf, output
import json

FIELD_TWITTER = "twitter"
FIELD_LINKEDIN = "linkedin"


PROMPT = f"""
As an SEO optimization assistant, your task is to evaluate an article provided within triple quotes. Analyze the technical accuracy of the content and its alignment with SEO best practices. Your analysis should culminate in the provision of:

1. Five announcements of a new article as the Twitter tweet with limit 30 words.
2. Five announcements of a new article as the LinkedIn post with limit 30 words.
3. Include a place for the link to an article in every announcement.

Please format your response as a JSON object with the following fields:
- "{FIELD_TWITTER}": An array of strings with announcements for Twitter. Example: ["Announcement 1", "Announcement 2"].
- "{FIELD_LINKEDIN}": An array of strings with announcements for LinkedIn. Example: ["Announcement 1", "Announcement 2"].
Ensure the response excludes extraneous formatting or labels, presenting only the JSON object for direct usability in Python.
"""


async def handle(chat_gpt: ChatGpt, filename: str):
    content = compress(pdf.read_pdf(filename))
    completion = await chat_gpt.get_completion(PROMPT, content, MODEL_GPT_4)

    completion_json = json.loads(completion)

    output.print_list_field(
        "💣 LinkedIn announcements:", FIELD_LINKEDIN, completion_json
    )

    output.print_list_field("🔥 Twitter announcements:", FIELD_TWITTER, completion_json)

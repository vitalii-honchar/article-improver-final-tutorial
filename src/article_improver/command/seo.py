from loguru import logger
from article_improver.chat_gpt.chat_gpt import ChatGpt, MODEL_GPT_4
from article_improver.chat_gpt.compressor import compress
from article_improver import pdf, output
import json

FIELD_SEO_OPTIMIZED_TITLES = "seo_optimized_titles"
FIELD_RATING = "rating"
FIELD_INCORRECT = "incorrect"
FIELD_STRONG_SIDES = "strong_sides"
FIELD_WEAK_SIDES = "weak_sides"
FIELD_IMPROVEMENTS = "improvements"

PROMPT = f"""
As an SEO optimization assistant, your task is to evaluate an article provided within triple quotes. Analyze the technical accuracy of the content and its alignment with SEO best practices. Your analysis should culminate in the provision of:

1. Ten SEO-optimized titles for the article, crafted to improve search engine visibility and attract more readers.
2. A numerical rating for the overall quality of the article on a scale from 1 to 10, considering factors such as relevance, readability, and SEO optimization.
3. Identification of the article's strengths and weaknesses, specifically highlighting three areas where the article excels and three aspects that need improvement.

Please format your response as a JSON object with the following fields:
- "{FIELD_SEO_OPTIMIZED_TITLES}": An array of strings containing three suggested titles. Example: ["SEO Optimized Title 1", "SEO Optimized Title 2", "SEO Optimized Title 3"].
- "{FIELD_RATING}": A string indicating the article's quality rating. Example: "7/10".
- "{FIELD_INCORRECT}": An array of strings listing any inaccuracies or technical errors found in the article. Example: ["Error 1", "Error 2", "Error 3"].
- "{FIELD_STRONG_SIDES}": An array of strings outlining the article's three main strengths. Example: ["Strength 1", "Strength 2", "Strength 3"].
- "{FIELD_WEAK_SIDES}": An array of strings detailing the article's three main weaknesses. Example: ["Weakness 1", "Weakness 2", "Weakness 3"].
- "{FIELD_IMPROVEMENTS}": An array of strings detailing the article's three points of improvements proposed by you. Example: ["Improvement 1", "Improvement 2", "Improvement 3"].
Ensure the response excludes extraneous formatting or labels, presenting only the JSON object for direct usability in Python.
"""


async def handle(chat_gpt: ChatGpt, filename: str):
    content = compress(pdf.read_pdf(filename))
    completion = await chat_gpt.get_completion(PROMPT, content, MODEL_GPT_4)
    logger.bind(completion=completion).info("response from chat gpt")

    completion_json = json.loads(completion)

    output.print_list_field(
        ":rocket: SEO optimized titles:", FIELD_SEO_OPTIMIZED_TITLES, completion_json
    )
    logger.info(f"🥇 Rating: {completion_json[FIELD_RATING]}")
    output.print_list_field(
        ":exploding_head: Incorrect sides:", FIELD_INCORRECT, completion_json
    )
    output.print_list_field(
        ":heavy_check_mark: Strong sides:", FIELD_STRONG_SIDES, completion_json
    )
    output.print_list_field(":x: Weak sides:", FIELD_WEAK_SIDES, completion_json)
    output.print_list_field(
        ":building_construction:  Improvements:", FIELD_IMPROVEMENTS, completion_json
    )

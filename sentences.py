import re

def split_text_to_sentences(text):
    # Regular expression pattern to match the separators with a preceding word character
    # and followed by a space or the end of the string to ensure correct sentence splitting
    pattern = r'(?<=\w)[.!?;:](?=\s|$)'
    # Use re.split() to split the text into sentences based on the pattern
    sentences = re.split(pattern, text)
    # Remove any leading/trailing whitespace from each sentence
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

text = """
As an SEO optimization assistant, your task is to evaluate an article provided within triple quotes. Analyze typos in the text and provide fix for the typos:

1. Fixed text without explanation of mistakes.
"""

# Split the provided text into sentences
sentences = split_text_to_sentences(text)

print(sentences)

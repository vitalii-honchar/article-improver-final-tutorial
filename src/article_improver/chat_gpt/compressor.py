import re

UNWANTED_SYMBOLS = [
    "\u2014",
    "\u2013",
    "\u2012",
    "\u2010",
    "\u2022",
    "\u2026",
    "\u00A0",
    "\u201C",
    "\u201D",
    "\u2018",
    "\u2019",
    "\u2122",
    "\u00AE",
    "\u00A9",
    "\u200a",
    "http:",
    "https:",
    "\n",
    "\t",
]

TEMPLATE_WITHOUT_PUNCTUATION = "[^a-zA-Z0-9\s,.!?;:']"

def remove_unwanted_symbols(content: str) -> str:
    for char in UNWANTED_SYMBOLS:
        content = content.replace(char, "")
    return content

def compress(content: str) -> str:
    content = remove_unwanted_symbols(content)
    return re.sub(TEMPLATE_WITHOUT_PUNCTUATION, "", content)

def compress_with_saving_punctuation(content: str) -> str:
    return remove_unwanted_symbols(content)
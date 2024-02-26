import fitz


def read_pdf(filename: str) -> str:
    with fitz.open(filename) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()

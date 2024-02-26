from article_improver import pdf
from uuid import uuid4
import pytest
import fitz


def test_return_text_if_file_reading_was_successful():
    # GIVEN
    filename = "tests/test.pdf"
    expected = "Test content"

    # WHEN
    actual = pdf.read_pdf(filename)

    # THEN
    assert actual == expected


def test_raise_exception_if_file_not_exists():
    # GIVEN
    filename = str(uuid4())

    # WHEN-THEN
    with pytest.raises(fitz.FileNotFoundError):
        pdf.read_pdf(filename)

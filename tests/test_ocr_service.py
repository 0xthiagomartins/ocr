import pytest
from src.service import perform_ocr


def test_perform_ocr():
    with open("tests/sample_image.png", "rb") as image_file:
        image_bytes = image_file.read()
        text = perform_ocr(image_bytes)
        assert "expected_text" in text


if __name__ == "__main__":
    pytest.main()

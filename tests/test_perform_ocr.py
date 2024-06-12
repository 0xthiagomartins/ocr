import pytest
from src.business import perform_ocr


def test_perform_ocr():
    with open("tests/sample_image.png", "rb") as image_file:
        image_bytes = image_file.read()
        text = perform_ocr(image_bytes)
        print(text)
        assert "This is a handwritten" in text


if __name__ == "__main__":
    pytest.main()

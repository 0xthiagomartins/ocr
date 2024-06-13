import pytest
from unittest.mock import patch
from confluent_kafka import KafkaError
from src.service import OCRService


@pytest.fixture
def mock_consumer():
    with patch("confluent_kafka.Consumer") as mock:
        yield mock


@pytest.fixture
def mock_producer():
    with patch("confluent_kafka.Producer") as mock:
        yield mock


@pytest.fixture
def mock_process_message():
    with patch("src.service.OCRService.process_message") as mock:
        yield mock


def test_consume_messages_normal(mock_consumer, mock_producer):
    mock_consumer_instance = mock_consumer.return_value
    mock_consumer_instance.poll.return_value = None

    ocr_service = OCRService({}, {}, "test_topic")
    ocr_service.consume_messages()

    mock_consumer_instance.subscribe.assert_called_once_with(["test_topic"])
    assert mock_consumer_instance.poll.called


def test_consume_messages_with_messages(
    mock_consumer, mock_process_message, mock_producer
):
    mock_consumer_instance = mock_consumer.return_value
    mock_producer_instance = mock_producer.return_value

    class MockMessage:
        def __init__(self, value, error=None):
            self._value = value
            self._error = error

        def value(self):
            return self._value

        def error(self):
            return self._error

    messages = [
        MockMessage(b"message1"),
        MockMessage(b"message2"),
        MockMessage(b"message3"),
    ]
    mock_consumer_instance.poll.side_effect = messages

    ocr_service = OCRService({}, {}, "test_topic")
    ocr_service.consume_messages()

    expected_calls = [call(b"message1"), call(b"message2"), call(b"message3")]
    assert mock_process_message.call_count == len(messages)
    mock_process_message.assert_has_calls(expected_calls)


def test_consume_messages_raises_exception(mock_consumer):
    mock_consumer_instance = mock_consumer.return_value

    class MockMessage:
        def __init__(self, value=None, error=None):
            self._value = value
            self._error = error

        def value(self):
            return self._value

        def error(self):
            return self._error

    mock_consumer_instance.poll.side_effect = [
        MockMessage(error=KafkaError(KafkaError._ALL_BROKERS_DOWN))
    ]

    ocr_service = OCRService({}, {}, "test_topic")
    ocr_service.consume_messages()

    assert mock_consumer_instance.poll.called


def test_consume_messages_specific_behavior(
    mock_consumer, mock_process_message, mock_producer
):
    mock_consumer_instance = mock_consumer.return_value
    mock_producer_instance = mock_producer.return_value

    class MockMessage:
        def __init__(self, value, error=None):
            self._value = value
            self._error = error

        def value(self):
            return self._value

        def error(self):
            return self._error

    messages = [
        MockMessage(b"message1"),
        MockMessage(b"special_message"),
        MockMessage(b"error_message"),
    ]
    mock_process_message.side_effect = [
        None,
        "special_message",
        Exception("Another exception"),
    ]
    mock_consumer_instance.poll.side_effect = messages

    ocr_service = OCRService({}, {}, "test_topic")
    ocr_service.consume_messages()

    assert mock_process_message.call_count == len(messages)
    assert mock_process_message.call_args_list[1][0][0] == b"special_message"

    with pytest.raises(Exception, match="Another exception"):
        ocr_service.consume_messages()


if __name__ == "__main__":
    pytest.main()

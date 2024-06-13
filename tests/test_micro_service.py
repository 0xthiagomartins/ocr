import pytest
from src.service import KafkaService
import logging


def test_kafka_service_consume(caplog):
    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "test-group",
        "auto.offset.reset": "earliest",
    }
    producer_config = {"bootstrap.servers": "localhost:9092"}

    kafka_service = KafkaService(consumer_config, producer_config)

    def mock_process_function(message):
        assert message == "test message"

    with caplog.at_level(logging.INFO):
        kafka_service.produce_message("test-topic", "test message")
        kafka_service.consume_messages(["test-topic"], mock_process_function)
        assert "Message produced to test-topic" in caplog.text


if __name__ == "__main__":
    pytest.main()

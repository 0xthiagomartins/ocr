from common import KafkaService, logger


class OCRService(KafkaService):
    def process_message(self, message):
        """
        Process a single message specifically for OCR.

        :param message: The message to process.
        """
        # Implement the OCR-specific processing logic here
        logger.info(f"Processing OCR message: {message}")
        # Simulate OCR processing
        processed_message = f"Processed OCR: {message.decode('utf-8')}"
        logger.info(f"Finished processing OCR message: {processed_message}")
        self.produce_message(processed_message)


if __name__ == "__main__":
    consumer_conf = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "ocr_consumer_group",
        "auto.offset.reset": "earliest",
    }

    producer_conf = {"bootstrap.servers": "localhost:9092"}

    topic = "ocr_topic"
    ocr_service = OCRService(consumer_conf, producer_conf, topic)
    ocr_service.consume_messages()

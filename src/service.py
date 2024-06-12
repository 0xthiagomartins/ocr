# src/service.py
from confluent_kafka import Consumer, Producer, KafkaError
import logging


class KafkaService:
    def __init__(self, consumer_config, producer_config):
        self.consumer = Consumer(consumer_config)
        self.producer = Producer(producer_config)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("KafkaService")

    def consume_messages(self, topics, process_function):
        self.consumer.subscribe(topics)
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        self.logger.info(
                            "End of partition reached %s [%d] at offset %d",
                            msg.topic(),
                            msg.partition(),
                            msg.offset(),
                        )
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    process_function(msg.value().decode("utf-8"))
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
        finally:
            self.consumer.close()

    def produce_message(self, topic, message):
        try:
            self.producer.produce(topic, message.encode("utf-8"))
            self.producer.flush()
            self.logger.info(f"Message produced to {topic}")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")


# Example process function
def process_message(message):
    print(f"Processing message: {message}")


if __name__ == "__main__":
    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "my-group",
        "auto.offset.reset": "earliest",
    }
    producer_config = {"bootstrap.servers": "localhost:9092"}

    kafka_service = KafkaService(consumer_config, producer_config)
    kafka_service.consume_messages(["my-topic"], process_message)

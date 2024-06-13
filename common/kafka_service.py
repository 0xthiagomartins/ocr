from confluent_kafka import Consumer, Producer, KafkaError
from .log import logger


class KafkaService:
    def __init__(self, consumer_conf, producer_conf, topic):
        self.consumer = Consumer(consumer_conf)
        self.producer = Producer(producer_conf)
        self.topic = topic
        self.consumer.subscribe([self.topic])

    def consume_messages(self):
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.info(
                            "End of partition reached {0}/{1}".format(
                                msg.topic(), msg.partition()
                            )
                        )
                    elif msg.error():
                        logger.error("Error occurred: {0}".format(msg.error().str()))
                else:
                    self.process_message(msg.value())
                    self.consumer.commit()
        except KeyboardInterrupt:
            logger.info("Stopping message consumer.")
        finally:
            self.consumer.close()

    def process_message(self, message):
        """
        Process a single message.
        This method should be overridden by subclasses.

        :param message: The message to process.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def produce_message(self, message):
        self.producer.produce(self.topic, key=None, value=message)
        self.producer.flush()

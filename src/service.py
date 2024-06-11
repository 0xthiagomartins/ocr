from kafka import KafkaConsumer, KafkaProducer
import json
from ocr_service import perform_ocr

KAFKA_BROKER = "kafka:9092"
INPUT_TOPIC = "input_topic"
OUTPUT_TOPIC = "output_topic"

consumer = KafkaConsumer(
    INPUT_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)


def consume_messages():
    for message in consumer:
        image_bytes = bytes(message.value["image"], encoding="utf-8")
        text = perform_ocr(image_bytes)
        producer.send(OUTPUT_TOPIC, value={"text": text})


if __name__ == "__main__":
    consume_messages()

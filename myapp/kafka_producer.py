from kafka import KafkaProducer
import json
from django.conf import settings

producer = KafkaProducer(
    bootstrap_servers=getattr(settings, "KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_quantity_update(product_id, new_quantity):
    data = {
        "product_id": product_id,
        "new_quantity": new_quantity
    }
    producer.send('product_quantity_update', value=data)

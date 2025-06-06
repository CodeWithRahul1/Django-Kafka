from kafka import KafkaConsumer
import json
import os
import sys
import django

# Add the base directory to the Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.conf import settings
from myapp.models import Product
from django.core.cache import cache

consumer = KafkaConsumer(
    settings.KAFKA_TOPIC,
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    print("Received message:", message.value)
    data = message.value
    product_id = data['product_id']
    new_quantity = data['new_quantity']

    try:
        product = Product.objects.get(id=product_id)
        product.quantity = new_quantity
        product.save()
        cache.set(f"product:{product_id}:quantity", new_quantity, timeout=300)
    except Product.DoesNotExist:
        pass

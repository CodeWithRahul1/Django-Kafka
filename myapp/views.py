from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import Product, Order
from django.contrib.auth.models import User
from .kafka_producer import send_quantity_update


@api_view(['POST'])
def create_order(request):
    product_id = request.data.get('product_id')
    user_id = request.data.get('user_id')
    quantity = int(request.data.get('quantity', 1))

    # Check cache first
    cache_key = f"product:{product_id}:quantity"
    cached_quantity = cache.get(cache_key)

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    available_quantity = cached_quantity if cached_quantity is not None else product.quantity

    if available_quantity < quantity:
        return Response({"error": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)

    # Create order
    user = User.objects.get(pk=user_id)
    order = Order.objects.create(product=product, user=user, quantity=quantity)

    # Update quantity in cache only
    new_quantity = available_quantity - quantity
    cache.set(cache_key, new_quantity, timeout=60 * 5)

    # Send Kafka message to sync DB + cache later
    send_quantity_update(product_id, new_quantity)

    return Response({"message": "Order created", "order_id": order.id})

@api_view(['GET'])
def get_product_by_id(request, product_id):
    cache_key = f"product:{product_id}"
    product_data = cache.get(cache_key)

    if product_data:
        return Response(product_data)

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)
    cache.set(cache_key, serializer.data, timeout=60*5)  # cache for 5 minutes

    return Response(serializer.data)

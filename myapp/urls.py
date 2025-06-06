from django.urls import path
from .views import get_product_by_id, create_order

urlpatterns = [
    path('product/<int:product_id>/', get_product_by_id, name='get-product'),
    path('order/', create_order, name='create_order'),
]

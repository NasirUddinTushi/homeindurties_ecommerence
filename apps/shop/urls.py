from django.urls import path
from .views import CartView, OrderListCreateView, OrderDetailView, AddToCartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('cart/add/', AddToCartView.as_view(), name='cart-add'),
]

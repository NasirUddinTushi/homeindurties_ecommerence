from django.urls import path
from .views import ProductReviewListAPIView, ReviewCreateAPIView, ReviewDetailAPIView

urlpatterns = [
    path('products/<int:product_id>/reviews/', ProductReviewListAPIView.as_view(), name='product-reviews'),
    path('reviews/add/', ReviewCreateAPIView.as_view(), name='add-review'),
    path('reviews/<int:pk>/', ReviewDetailAPIView.as_view(), name='update-delete-review'),
]
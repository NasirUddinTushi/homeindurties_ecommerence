from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

def custom_response(success=True, message="", data=None, status_code=200):
    return Response({
        "success": success,
        "message": message,
        "data": data or {},
        "status": status_code
    }, status=status_code)

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_published=True)
        serializer = ProductSerializer(products, many=True)
        return custom_response(
            success=True,
            message="Published products retrieved successfully.",
            data=serializer.data
        )

class ProductDetailView(APIView):
    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug, is_published=True)
            serializer = ProductSerializer(product)
            return custom_response(
                success=True,
                message="Product detail retrieved successfully.",
                data=serializer.data
            )
        except Product.DoesNotExist:
            return custom_response(
                success=False,
                message="Product not found.",
                status_code=404
            )

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.filter(is_active=True)
        serializer = CategorySerializer(categories, many=True)
        return custom_response(
            success=True,
            message="Categories retrieved successfully.",
            data=serializer.data
        )

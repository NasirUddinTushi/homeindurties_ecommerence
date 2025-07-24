from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.products.models import Product
from .models import Cart, CartItem, Order, OrderItem, ShippingAddress, Payment
from .serializers import CartSerializer, OrderSerializer

# Optional: If using custom user
from django.contrib.auth import get_user_model
User = get_user_model()


def custom_response(success=True, message="", data=None, status_code=200):
    return Response({
        "success": success,
        "message": message,
        "data": data or {},
        "status": status_code
    }, status=status_code)

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            product_id = int(request.data.get("product_id"))
            quantity = int(request.data.get("quantity", 1))
        except (TypeError, ValueError):
            return Response({
                "success": False,
                "message": "Invalid product ID or quantity.",
                "data": {},
                "status": 400
            }, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({
                "success": False,
                "message": "Product not found",
                "data": {},
                "status": 404
            }, status=404)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({
            "success": True,
            "message": "Product added to cart successfully.",
            "data": {
                "product": product.title,
                "quantity": cart_item.quantity
            },
            "status": 200
        }, status=200)



class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return custom_response(
            message="Cart retrieved successfully.",
            data=serializer.data
        )


class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return custom_response(
            message="Order list fetched.",
            data=serializer.data
        )

    def post(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        if not cart or not cart.items.exists():
            return custom_response(
                success=False,
                message="Cart is empty.",
                status_code=400
            )

        data = request.data
        payment_method = data.get("payment_method")
        if payment_method != "cod":
            return custom_response(
                success=False,
                message="Only Cash on Delivery is supported currently.",
                status_code=400
            )

        address_data = data.get("shipping_address")
        if not address_data:
            return custom_response(
                success=False,
                message="Shipping address is required.",
                status_code=400
            )

        # Calculate total
        total = sum(item.product.price * item.quantity for item in cart.items.all())

        # Create Order
        order = Order.objects.create(user=user, total_amount=total)

        # Create Order Items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Save Shipping Address
        ShippingAddress.objects.create(order=order, **address_data)

        # Create Payment record (not paid yet for COD)
        Payment.objects.create(
            order=order,
            method="cod",
            transaction_id="COD-{}".format(order.id),
            is_paid=False
        )

        # Clear cart
        cart.items.all().delete()

        return custom_response(
            message="Order placed successfully with Cash on Delivery.",
            data={"order_id": order.id},
            status_code=201
        )

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
            serializer = OrderSerializer(order)
            return custom_response(
                message="Order detail retrieved.",
                data=serializer.data
            )
        except Order.DoesNotExist:
            return custom_response(
                success=False,
                message="Order not found.",
                status_code=404
            )

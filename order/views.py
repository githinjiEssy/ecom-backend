from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from product.models import Product
from .models import Order


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createOrder(request):
    user = request.user
    product_id = request.data.get('product_id')

    if not product_id:
        return Response(
            {"error": "Product ID is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    order_data = {
        "product": product.id,
        "status": request.data.get("status", "pending"),
    }

    serializer = OrderSerializer(data=order_data)
    if serializer.is_valid():
        order = serializer.save(user=user)
        return Response(
            {"message": "Order created successfully", "order": OrderSerializer(order).data},
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateStatus(request):
    user = request.user
    user_role = getattr(user, "role", "user")

    if user_role != "admin":
        return Response(
            {"error": "Only admins can update order status"},
            status=status.HTTP_403_FORBIDDEN
        )

    order_id = request.data.get('order_id')
    new_status = request.data.get('status')

    if not order_id or not new_status:
        return Response(
            {"error": "order_id and status are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = OrderSerializer(order, data={'status': new_status}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Order status updated successfully", "order": serializer.data},
            status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





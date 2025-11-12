from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from decouple import config
import requests
from .serializers import MpesaSerializer
from product.models import Product


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    user = request.user

    product_id = request.data.get("product_id")
    if not product_id:
        return Response({"error": "product_id is required"}, status=400)

    product = Product.objects.get(id=product_id)
    amount = product.product_price

    phone_number = user.phone_number
    serializer = MpesaSerializer()

    try:
        token = serializer.generate_access_token()
        password, timestamp = serializer.generate_password()
    except Exception:
        return Response({"error": "Token or password generation failed"}, status=500)

    stk_push_url = config("STK_PUSH_API")

    request_data = {
        "BusinessShortCode": config("BIZSHORTCODE"),
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": config("BIZSHORTCODE"),
        "PhoneNumber": phone_number,
        "CallBackURL": config("CALLBACK_URL"),
        "AccountReference": "Order Payment",
        "TransactionDesc": "Payment"
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(stk_push_url, json=request_data, headers=headers)

        mpesa_response = response.json()

        if mpesa_response.get("ResponseCode") == "0":
            Mpesa.objects.create(
                user=user,
                product=product,
                amount=amount,
                transaction_id=mpesa_response.get("CheckoutRequestID")
            )

        return Response(mpesa_response, status=response.status_code)

    except Exception:
        return Response({"error": "Failed to initiate payment"}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def mpesa_callback(request):
    data = request.data["Body"]["stkCallback"]
    checkout_id = data["CheckoutRequestID"]
    result_code = data["ResultCode"]

    if result_code == 0:
        items = data["CallbackMetadata"]["Item"]
        
        amount = next(item["Value"] for item in items if item["Name"] == "Amount")
        receipt = next(item["Value"] for item in items if item["Name"] == "MpesaReceiptNumber")

        Mpesa.objects.filter(transaction_id=checkout_id).update(
            amount=amount,
            transaction_id=receipt  
        )

    return Response({"message": "Callback received"})

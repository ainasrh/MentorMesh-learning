
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import CreatePaymentSerializer, VerifyPaymentSerializer
from .razorpay_utils import create_razorpay_order, verify_signature
from .payment_publisher import publish_payment_success

class CreateOrder(APIView):
    def post(self, request):
        serializer = CreatePaymentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            order = create_razorpay_order(data['amount'], f"rcpt_{data['user_id']}_{data['course_id']}")
            payment = Payment.objects.create(
                user_id=data['user_id'],
                course_id=data['course_id'],
                order_id=order['id'],
                amount=data['amount']
            )
            return Response(order, status=200)
        return Response(serializer.errors, status=400)

class VerifyPayment(APIView):
    def post(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                payment = Payment.objects.get(order_id=data['order_id'])
            except Payment.DoesNotExist:
                return Response({"error": "Invalid order_id"}, status=400)

            is_valid = verify_signature(data['order_id'], data['payment_id'], data['signature'])
            if is_valid:
                payment.payment_id = data['payment_id']
                payment.signature = data['signature']
                payment.is_successful = True
                payment.save()
                
                publish_payment_success(user_id=payment.user_id, course_id=payment.course_id)
                
                

                return Response({"message": "Payment verified"}, status=200)
            else:
                return Response({"error": "Signature mismatch"}, status=400)
        return Response(serializer.errors, status=400)

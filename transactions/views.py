from rest_framework.views import APIView, Response
from rest_framework import status

from transactions.payment_processor import process_payments
from transactions.serializers.payment_serializer import PaymentSerializer


class Payments(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data, many=True)

        if not serializer.is_valid():
            return Response(
                data={"error": "invalid payload"},
                status=status.HTTP_400_BAD_REQUEST
            )

        resp = process_payments(serializer.data)

        return Response(resp)



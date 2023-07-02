from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    currency = serializers.CharField(max_length=10)

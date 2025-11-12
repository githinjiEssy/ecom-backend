from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'status', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate_status(self, value):
        allowed_statuses = ["pending", "completed", "cancelled"]

        if value.lower() not in allowed_statuses:
            raise serializers.ValidationError(
                "Invalid status."
            )

        return value.lower()

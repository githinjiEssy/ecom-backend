from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'phone_number', 'role', 'is_active', 'is_staff', 'date_registered']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if not value.endswith("@gmail.com"): 
            raise serializers.ValidationError("Only @gmail.com emails are allowed.")
        return value
    
    def validate_role(self, value):
        roles = [
            "user", "admin"
        ]

        if value not in roles:
            raise serializers.ValidationError("Invalid role input")

    def create(self, validated_data):
        raw_password = validated_data['password']
        validated_data['password'] = make_password(raw_password)
        user = super().create(validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            validated_data['password'] = make_password(password)
        return super().update(instance, validated_data)
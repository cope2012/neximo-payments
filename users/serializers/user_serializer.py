import logging

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import User

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "password",
        )
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if password := attrs.get("password"):
            attrs["password"] = make_password(password)

        return super().validate(attrs)

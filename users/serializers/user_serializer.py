from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User


class CreateUserSerializer(serializers.ModelSerializer):
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


class UpdatePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    old_password = serializers.CharField()

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['new_password'])
        instance.save()

    def validate(self, attrs):
        user = self.context['user']

        if not user.check_password(attrs['old_password']):
            raise ValidationError('passwords dont match')

        return super().validate(attrs)

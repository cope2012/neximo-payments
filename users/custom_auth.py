import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model


class CustomAuth(BaseAuthentication):
    def authenticate(self, request):
        usr_cls = get_user_model()

        if authorization_header := request.headers.get('Authorization'):
            try:
                access_token = authorization_header.split(' ')[1]
                payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('token is expired')
            except IndexError:
                raise exceptions.AuthenticationFailed('missing auth prefix')

            user = usr_cls.objects.filter(id=payload['user_id']).first()
            if user is None:
                raise exceptions.AuthenticationFailed('User not found')

            return user, None
        else:
            return None

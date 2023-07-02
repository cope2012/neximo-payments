from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers.user_serializer import UserSerializer
from .models import User


class Register(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()

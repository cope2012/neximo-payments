from rest_framework.generics import CreateAPIView
from .serializers.user_serializer import UserSerializer
from .models import User


class Register(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

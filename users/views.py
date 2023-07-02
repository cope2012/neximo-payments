from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, Response, status


from .serializers.user_serializer import CreateUserSerializer, UpdatePasswordSerializer
from .models import User


class Register(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()


class ChangePassword(APIView):
    def post(self, request):
        serializer = UpdatePasswordSerializer(
            data=request.data,
            context={
                'user': request.user
            }
        )

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer.update(self.request.user, request.data)

        return Response()

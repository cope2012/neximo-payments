from django.urls import path
from .views import Register, ChangePassword
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register', Register.as_view()),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('password', ChangePassword.as_view()),
]

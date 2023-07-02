from django.urls import path
from .views import Register
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register', Register.as_view()),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]

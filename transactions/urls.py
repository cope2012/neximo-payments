from django.urls import path
from .views import Payments

urlpatterns = [
    path("payments", Payments.as_view()),
]

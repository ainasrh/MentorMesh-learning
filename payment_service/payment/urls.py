from django.urls import path
from .views import *

urlpatterns=[
    path("create-payment/", CreateOrder.as_view()),
    path("verify-payment/", VerifyPayment.as_view())

]
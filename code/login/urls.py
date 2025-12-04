from django.urls import path
from .views import LoginView

urlpatterns = [
    path('', LoginView.index),
    path('login/', LoginView.login, name='login')
]
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenView,RegisterView



urlpatterns = [
    path('register',RegisterView.as_view(), name='register'),
    path('token/',CustomTokenView.as_view(), name ='token'),
    path('token/refresh/',TokenRefreshView.as_view(), name='refresh_token'),
]
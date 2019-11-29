from django.urls import path, include
from rest_framework_simplejwt import views


urlpatterns = [
    path('login', views.TokenObtainPairView.as_view()),
    path('refresh', views.TokenRefreshView.as_view()),
    path('verify', views.TokenVerifyView.as_view())
]

from django.urls import path

from app.accounts.api_v1 import views

urlpatterns = [
    path('accounts', views.AccountCreate.as_view()),
    path('accounts/my-account', views.AccountRUD.as_view()),
]

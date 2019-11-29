from app.accounts import models
from app.accounts.api_v1 import serializer
from app.shared.logger import Logger
from app.shared.permissions import AllowAny, IsAuthenticated
from rest_framework import generics


class AccountCreate(generics.CreateAPIView):
    queryset = models.Account.objects.all()
    serializer_class = serializer.AccountCreate
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        Logger.info('User create request', request=request)
        return super().post(request, *args, **kwargs)


class AccountRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Account.objects.all()
    serializer_class = serializer.Account
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        Logger.info('User requested', request=self.request)
        return models.Account.objects.get(
            pk=self.request.headers['userId']
        )

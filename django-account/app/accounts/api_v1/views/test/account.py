from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from app.accounts.api_v1.serializer.account import Account as AccountSerializer
from app.accounts.api_v1.serializer.account import \
    AccountCreate as AccountCreateSerializer
from app.accounts.models.account import Account as AccountModel


class AccountViewsTest(APITestCase):
    def test_create_valid_basic_account(self):
        response = self.client.post('/v1/accounts', {
            "email": 'teste@hotmail.com',
            "password": "test@123"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(response.data.keys()), set([
            'last_name', 'gender', 'first_name', 'id', 'birthdate',
            'groups', 'user_permissions', 'last_login', 'date_joined',
            'is_active', 'email'
        ]))

    def test_create_invalid_basic_account(self):
        response = self.client.post('/v1/accounts', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data.keys()), set(['password', 'email']))

    def test_create_account_not_allowed_methods(self):
        response = self.client.get('/v1/accounts', {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put('/v1/accounts', {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch('/v1/accounts', {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete('/v1/accounts', {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_valid_account(self):
        account = AccountModel.objects.create_superuser(
            email='teste@hotmail.com',
            password='test@123'
        )
        response = self.client.get('/v1/accounts/my-account', **{
            'HTTP_AUTH': 'true', 'HTTP_USERID': account.pk
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data.keys()), set([
            'last_name', 'gender', 'first_name', 'id', 'birthdate',
            'groups', 'user_permissions', 'last_login', 'date_joined',
            'is_active', 'email', 'username'
        ]))

    def test_get_valid_account_without_authentication(self):
        account = AccountModel.objects.create_superuser(
            email='teste@hotmail.com',
            password='test@123'
        )

        response = self.client.get('/v1/accounts/my-account')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_valid_account(self):
        account = AccountModel.objects.create_superuser(
            email='teste@hotmail.com',
            password='test@123'
        )
        response = self.client.patch('/v1/accounts/my-account', {
            'gender': 'male',
        }, **{
            'HTTP_AUTH': 'true', 'HTTP_USERID': account.pk
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data.keys()), set([
            'last_name', 'gender', 'first_name', 'id', 'birthdate',
            'groups', 'user_permissions', 'last_login', 'date_joined',
            'is_active', 'email', 'username'
        ]))
        self.assertEqual(response.data['gender'], 'male')

    def test_get_account_not_allowed_methods(self):
        response = self.client.post('/v1/accounts/my-account', {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post('/v1/accounts/my-account', {}, **{
            'HTTP_AUTH': 'true', 'HTTP_USERID': 1
        })
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

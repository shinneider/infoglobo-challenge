from django.test import TestCase

from app.accounts.api_v1.serializer.account import Account as AccountSerializer
from app.accounts.api_v1.serializer.account import \
    AccountCreate as AccountCreateSerializer
from app.accounts.models.account import Account as AccountModel


class AccountSerializerTest(TestCase):

    def test_visible_fields_account_serializer(self):
        account = AccountModel.objects.create_account(
            email='teste@hotmail.com',
            password='test@123'
        )

        serializer = AccountSerializer(instance=account)
        self.assertEqual(set(serializer.data.keys()), set([
            'id', 'last_login', 'email', 'gender', 'user_permissions',
            'groups', 'is_active', 'date_joined', 'birthdate',
            'first_name', 'last_name', 'username'
        ]))

    def test_change_field_without_password_account_serializer(self):
        account = AccountModel.objects.create_account(
            email='teste@hotmail.com',
            password='test@123'
        )
        password = account.password
        self.assertEqual(account.username, '')

        serializer = AccountSerializer(instance=account, partial=True, data={
            "username": 'test123'
        })
        self.assertEqual(serializer.is_valid(), True)

        serializer.save()
        self.assertEqual(account.username, 'test123')
        self.assertEqual(account.password, password)

    def test_change_field_with_password_account_serializer(self):
        account = AccountModel.objects.create_account(
            email='teste@hotmail.com',
            password='test@123'
        )
        password = account.password
        self.assertEqual(account.username, '')

        serializer = AccountSerializer(instance=account, partial=True, data={
            "username": 'test123',
            "password": 'test1234'
        })
        self.assertEqual(serializer.is_valid(), True)

        serializer.save()
        self.assertEqual(account.username, 'test123')
        self.assertNotEqual(account.password, password)

    def test_visible_fields_account_serializer(self):
        account = AccountModel.objects.create_account(
            email='teste@hotmail.com',
            password='test@123'
        )

        serializer = AccountCreateSerializer(instance=account)
        self.assertEqual(set(serializer.data.keys()), set([
            'id', 'last_login', 'email', 'gender', 'user_permissions',
            'groups', 'is_active', 'date_joined', 'birthdate',
            'first_name', 'last_name'
        ]))

    def test_visible_fields_account_serializer(self):
        serializer = AccountCreateSerializer(data={
            "email": 'teste@hotmail.com',
            "password": 'test@123'
        })
        self.assertEqual(serializer.is_valid(), True)

        account = serializer.save()
        self.assertEqual(account.pk, 3)

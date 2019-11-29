from django.test import TestCase

from app.accounts.models.account import Account


class AccountModelTest(TestCase):

    # Valid cases

    def test_create_valid_basic_account(self):
        try:
            account = Account.objects.create_account(
                email='teste@hotmail.com',
                password='test@123'
            )

            self.assertEqual(account.is_staff, False)
            self.assertEqual(account.is_superuser, False)
        except:
            self.fail('Creation of Basic Account failed.')

    def test_create_valid_superuser_account(self):
        try:
            account = Account.objects.create_superuser(
                email='teste@hotmail.com',
                password='test@123'
            )

            self.assertEqual(account.is_staff, True)
            self.assertEqual(account.is_superuser, True)
        except:
            self.fail('Creation of Super Account failed.')

    def test_create_valid_gender_account(self):
        try:
            Account.objects.create_superuser(
                email='teste@hotmail.com',
                password='test@123',
                gender='male'
            )

            Account.objects.create_superuser(
                email='teste2@hotmail.com',
                password='test@123',
                gender='female'
            )

        except:
            self.fail('Creation of Super Account failed.')

    def test_create_valid_birthdate_account(self):
        from datetime import datetime

        try:
            Account.objects.create_superuser(
                email='teste@hotmail.com',
                password='test@123',
                birthdate=datetime.now()
            )

        except:
            self.fail('Creation of Super Account failed.')

    # Invalid cases
    def test_create_invalid_basic_account(self):
        try:
            account = Account.objects.create_account(
                email=None,
                password='teste@123'
            )
            self.fail('Creation of Basic Account without a email is a error.')
        except:
            pass

    def test_create_repeted_email_account(self):
        from django.db.utils import IntegrityError

        try:
            Account.objects.create_account(
                email='teste@hotmail.com',
                password='test@123'
            )

            Account.objects.create_account(
                email='teste@hotmail.com',
                password='test@123'
            )

        except IntegrityError:
            # All ok generate unique error
            pass

        except:
            self.fail('Creation of Account with same email works, it`s a error!')

    def test_create_username_account_with_name(self):
        account1 = Account.objects.create_account(
            email='teste@hotmail.com',
            password='test@123',
            first_name='test',
            last_name='test'
        )

        account2 = Account.objects.create_account(
            email='teste2@hotmail.com',
            password='test@123',
            first_name='test',
            last_name='test2'
        )

        self.assertEqual(account1.username, 'test.test')
        self.assertEqual(account2.username, 'test.test2')

    def test_create_username_account_with_same_name(self):
        account1 = Account.objects.create_account(
            email='teste@hotmail.com',
            password='test@123',
            first_name='test',
            last_name='test'
        )

        account2 = Account.objects.create_account(
            email='teste2@hotmail.com',
            password='test@123',
            first_name='test',
            last_name='test'
        )

        self.assertEqual(account1.username, 'test.test')
        self.assertEqual(account2.username, 'test.test.2')

    def test_create_username_account_without_name(self):
        account1 = Account.objects.create_account(
            email='teste@hotmail.com',
            password='test@123'
        )

        account2 = Account.objects.create_account(
            email='teste2@hotmail.com',
            password='test@123'
        )

        self.assertEqual(account1.username, '')
        self.assertEqual(account2.username, '.2')
